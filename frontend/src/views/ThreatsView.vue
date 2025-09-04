<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Threat Intelligence</h1>
        <p class="text-gray-600">Browse and analyze threat indicators</p>
      </div>
      <div class="flex items-center space-x-3">
        <button
          @click="refreshThreats"
          :disabled="loading"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
        >
          <RefreshCw :class="['w-4 h-4 mr-2', loading && 'animate-spin']" />
          Refresh
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Filters</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Severity</label>
          <select
            v-model="filters.severity"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
          >
            <option value="">All Severities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
          <select
            v-model="filters.type"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
          >
            <option value="">All Types</option>
            <option value="ip">IP Address</option>
            <option value="domain">Domain</option>
            <option value="url">URL</option>
            <option value="file_hash">File Hash</option>
            <option value="cve">CVE</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Source</label>
          <select
            v-model="filters.source"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
          >
            <option value="">All Sources</option>
            <option value="AbuseIPDB">AbuseIPDB</option>
            <option value="CISA_KEV">CISA KEV</option>
            <option value="NVD">NVD</option>
            <option value="MalwareBazaar">MalwareBazaar</option>
            <option value="URLhaus">URLhaus</option>
          </select>
        </div>
        
        <div class="flex items-end">
          <label class="flex items-center">
            <input
              type="checkbox"
              v-model="filters.activeOnly"
              @change="applyFilters"
              class="rounded border-gray-300 text-red-600 shadow-sm focus:border-red-300 focus:ring focus:ring-red-200 focus:ring-opacity-50"
            >
            <span class="ml-2 text-sm text-gray-700">Active only</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <Shield class="h-8 w-8 text-blue-600" />
          </div>
          <div class="ml-5 w-0 flex-1">
            <dl>
              <dt class="text-sm font-medium text-gray-500 truncate">Total Threats</dt>
              <dd class="text-lg font-medium text-gray-900">{{ stats?.total_threats || 0 }}</dd>
            </dl>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <AlertTriangle class="h-8 w-8 text-orange-600" />
          </div>
          <div class="ml-5 w-0 flex-1">
            <dl>
              <dt class="text-sm font-medium text-gray-500 truncate">Active Threats</dt>
              <dd class="text-lg font-medium text-gray-900">{{ stats?.active_threats || 0 }}</dd>
            </dl>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <Clock class="h-8 w-8 text-green-600" />
          </div>
          <div class="ml-5 w-0 flex-1">
            <dl>
              <dt class="text-sm font-medium text-gray-500 truncate">Recent (24h)</dt>
              <dd class="text-lg font-medium text-gray-900">{{ stats?.recent_threats_24h || 0 }}</dd>
            </dl>
          </div>
        </div>
      </div>
    </div>

    <!-- Threats Table -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Threat Indicators</h3>
      </div>
      
      <div v-if="loading" class="p-6">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 5" :key="i" class="h-16 bg-gray-200 rounded"></div>
        </div>
      </div>
      
      <div v-else-if="threats.length === 0" class="p-6 text-center">
        <Search class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p class="text-gray-500">No threats found matching your criteria</p>
      </div>
      
      <div v-else class="overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Indicator
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Severity
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Confidence
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Seen
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="threat in threats" :key="threat.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm font-medium text-gray-900 font-mono">
                    {{ threat.value }}
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <TypeBadge :type="threat.type" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <SeverityBadge :severity="threat.severity" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ threat.source }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm text-gray-900">{{ threat.confidence }}%</div>
                  <div class="ml-2 w-16 bg-gray-200 rounded-full h-2">
                    <div
                      class="bg-blue-600 h-2 rounded-full"
                      :style="{ width: `${threat.confidence}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatTimeAgo(threat.last_seen) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewThreat(threat)"
                  class="text-red-600 hover:text-red-900"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="previousPage"
            :disabled="pagination.page <= 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="nextPage"
            :disabled="!hasNextPage"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing page <span class="font-medium">{{ pagination.page }}</span>
              of <span class="font-medium">{{ totalPages }}</span>
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button
                @click="previousPage"
                :disabled="pagination.page <= 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                <ChevronLeft class="h-5 w-5" />
              </button>
              <button
                @click="nextPage"
                :disabled="!hasNextPage"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                <ChevronRight class="h-5 w-5" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Threat Detail Modal -->
    <ThreatDetailModal
      v-if="selectedThreat"
      :threat="selectedThreat"
      @close="selectedThreat = null"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useThreatsStore } from '@/stores/threats'
import { formatDistanceToNow } from 'date-fns'
import { useToast } from 'vue-toastification'
import {
  RefreshCw, Shield, AlertTriangle, Clock, Search,
  ChevronLeft, ChevronRight
} from 'lucide-vue-next'

import SeverityBadge from '@/components/SeverityBadge.vue'
import TypeBadge from '@/components/TypeBadge.vue'
import ThreatDetailModal from '@/components/ThreatDetailModal.vue'

export default {
  name: 'ThreatsView',
  components: {
    SeverityBadge,
    TypeBadge,
    ThreatDetailModal,
    RefreshCw,
    Shield,
    AlertTriangle,
    Clock,
    Search,
    ChevronLeft,
    ChevronRight
  },
  setup() {
    const threatsStore = useThreatsStore()
    const toast = useToast()
    const selectedThreat = ref(null)

    const filters = reactive({
      severity: '',
      type: '',
      source: '',
      activeOnly: true
    })

    const loading = computed(() => threatsStore.loading)
    const threats = computed(() => threatsStore.threats)
    const stats = computed(() => threatsStore.stats)
    const pagination = computed(() => threatsStore.pagination)

    const totalPages = computed(() => {
      return Math.ceil(pagination.value.total / pagination.value.limit)
    })

    const hasNextPage = computed(() => {
      return pagination.value.page < totalPages.value
    })

    const refreshThreats = async () => {
      try {
        await Promise.all([
          threatsStore.fetchThreats(),
          threatsStore.fetchStats()
        ])
        toast.success('Threats updated successfully')
      } catch (error) {
        toast.error('Failed to refresh threats')
      }
    }

    const applyFilters = async () => {
      threatsStore.setFilters(filters)
      await threatsStore.fetchThreats()
    }

    const previousPage = async () => {
      if (pagination.value.page > 1) {
        threatsStore.setPage(pagination.value.page - 1)
        await threatsStore.fetchThreats()
      }
    }

    const nextPage = async () => {
      if (hasNextPage.value) {
        threatsStore.setPage(pagination.value.page + 1)
        await threatsStore.fetchThreats()
      }
    }

    const viewThreat = (threat) => {
      selectedThreat.value = threat
    }

    const formatTimeAgo = (dateString) => {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true })
    }

    onMounted(async () => {
      await refreshThreats()
    })

    return {
      loading,
      threats,
      stats,
      pagination,
      filters,
      selectedThreat,
      totalPages,
      hasNextPage,
      refreshThreats,
      applyFilters,
      previousPage,
      nextPage,
      viewThreat,
      formatTimeAgo
    }
  }
}
</script>
