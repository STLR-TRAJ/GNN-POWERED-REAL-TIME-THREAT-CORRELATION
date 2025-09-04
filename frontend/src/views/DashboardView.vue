<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Threat Intelligence Dashboard</h1>
        <p class="text-gray-600">Real-time overview of your cybersecurity posture</p>
      </div>
      <div class="flex items-center space-x-3">
        <button
          @click="refreshData"
          :disabled="loading"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
        >
          <RefreshCw :class="['w-4 h-4 mr-2', loading && 'animate-spin']" />
          Refresh
        </button>
        <div class="flex items-center space-x-2 text-sm text-gray-500">
          <div :class="['w-2 h-2 rounded-full', isHealthy ? 'bg-green-400' : 'bg-red-400']"></div>
          <span>{{ isHealthy ? 'System Healthy' : 'System Issues' }}</span>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <SummaryCard
        title="Total Threats"
        :value="summary?.summary?.total_threats || 0"
        icon="Shield"
        color="blue"
      />
      <SummaryCard
        title="Active Threats"
        :value="summary?.summary?.active_threats || 0"
        icon="AlertTriangle"
        color="orange"
      />
      <SummaryCard
        title="Critical Alerts"
        :value="summary?.summary?.critical_alerts || 0"
        icon="AlertOctagon"
        color="red"
      />
      <SummaryCard
        title="Recent (24h)"
        :value="summary?.summary?.recent_threats_24h || 0"
        :trend="threatTrend"
        icon="TrendingUp"
        color="green"
      />
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Threats by Severity -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Threats by Severity</h3>
        <SeverityChart :data="summary?.threats_by_severity || {}" />
      </div>

      <!-- Threats by Type -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Threats by Type</h3>
        <TypeChart :data="summary?.threats_by_type || {}" />
      </div>
    </div>

    <!-- Recent Activity and Critical Threats -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Critical Threats -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Critical Threats</h3>
          <p class="text-sm text-gray-500">Threats requiring immediate attention</p>
        </div>
        <div class="p-6">
          <div v-if="summary?.recent_critical_threats?.length" class="space-y-4">
            <ThreatCard
              v-for="threat in summary.recent_critical_threats"
              :key="threat.id"
              :threat="threat"
              compact
            />
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <ShieldCheck class="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No critical threats detected</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Recent Activity</h3>
          <p class="text-sm text-gray-500">Latest threats and alerts</p>
        </div>
        <div class="p-6">
          <div v-if="recentActivity?.recent_threats?.length" class="space-y-3">
            <div
              v-for="threat in recentActivity.recent_threats.slice(0, 5)"
              :key="threat.id"
              class="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0"
            >
              <div class="flex items-center space-x-3">
                <SeverityBadge :severity="threat.severity" size="sm" />
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ threat.value }}</p>
                  <p class="text-xs text-gray-500">{{ threat.source }}</p>
                </div>
              </div>
              <div class="text-xs text-gray-400">
                {{ formatTimeAgo(threat.created_at) }}
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <Activity class="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No recent activity</p>
          </div>
        </div>
      </div>
    </div>

    <!-- System Status -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">System Status</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="(status, component) in healthStatus?.components || {}"
          :key="component"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center space-x-2">
            <div :class="[
              'w-2 h-2 rounded-full',
              status === 'healthy' || status === 'operational' ? 'bg-green-400' : 'bg-red-400'
            ]"></div>
            <span class="text-sm font-medium text-gray-700 capitalize">{{ component.replace('_', ' ') }}</span>
          </div>
          <span :class="[
            'text-xs px-2 py-1 rounded-full',
            status === 'healthy' || status === 'operational' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          ]">
            {{ status }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { formatDistanceToNow } from 'date-fns'
import { useToast } from 'vue-toastification'
import {
  RefreshCw, Shield, AlertTriangle, AlertOctagon, TrendingUp,
  ShieldCheck, Activity
} from 'lucide-vue-next'

import SummaryCard from '@/components/SummaryCard.vue'
import ThreatCard from '@/components/ThreatCard.vue'
import SeverityBadge from '@/components/SeverityBadge.vue'
import SeverityChart from '@/components/SeverityChart.vue'
import TypeChart from '@/components/TypeChart.vue'

export default {
  name: 'DashboardView',
  components: {
    SummaryCard,
    ThreatCard,
    SeverityBadge,
    SeverityChart,
    TypeChart,
    RefreshCw,
    Shield,
    AlertTriangle,
    AlertOctagon,
    TrendingUp,
    ShieldCheck,
    Activity
  },
  setup() {
    const dashboardStore = useDashboardStore()
    const toast = useToast()
    let refreshInterval = null

    const loading = computed(() => dashboardStore.loading)
    const summary = computed(() => dashboardStore.summary)
    const recentActivity = computed(() => dashboardStore.recentActivity)
    const healthStatus = computed(() => dashboardStore.healthStatus)
    const isHealthy = computed(() => dashboardStore.isHealthy)
    const threatTrend = computed(() => dashboardStore.threatTrend)

    const refreshData = async () => {
      try {
        await dashboardStore.refreshAll()
        toast.success('Dashboard updated successfully')
      } catch (error) {
        toast.error('Failed to refresh dashboard')
      }
    }

    const formatTimeAgo = (dateString) => {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true })
    }

    onMounted(async () => {
      // Initial load
      await refreshData()
      
      // Set up auto-refresh every 5 minutes
      refreshInterval = setInterval(async () => {
        await dashboardStore.refreshAll()
      }, 5 * 60 * 1000)
    })

    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }
    })

    return {
      loading,
      summary,
      recentActivity,
      healthStatus,
      isHealthy,
      threatTrend,
      refreshData,
      formatTimeAgo
    }
  }
}
</script>
