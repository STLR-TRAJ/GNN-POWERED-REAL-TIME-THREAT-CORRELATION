<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Alert Management</h1>
        <p class="text-gray-600">Configure email alerts and notification settings</p>
      </div>
      <div class="flex items-center space-x-3">
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          <Plus class="w-4 h-4 mr-2" />
          New Configuration
        </button>
      </div>
    </div>

    <!-- Alert Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Mail class="h-8 w-8 text-blue-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Alerts</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats?.total_alerts || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CheckCircle class="h-8 w-8 text-green-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Alerts Sent</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats?.alerts_sent || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <XCircle class="h-8 w-8 text-red-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Failed Alerts</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats?.alerts_failed || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Clock class="h-8 w-8 text-orange-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Recent (24h)</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats?.recent_alerts_24h || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert Configurations -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Alert Configurations</h3>
        <p class="text-sm text-gray-500 mt-1">Manage email alert settings and recipients</p>
      </div>
      
      <div v-if="loading" class="p-6">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 3" :key="i" class="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
      
      <div v-else-if="configurations.length === 0" class="p-6 text-center">
        <Mail class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p class="text-gray-500">No alert configurations found</p>
        <button
          @click="showCreateModal = true"
          class="mt-3 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200"
        >
          Create your first configuration
        </button>
      </div>
      
      <div v-else class="divide-y divide-gray-200">
        <div
          v-for="config in configurations"
          :key="config.id"
          class="p-6 hover:bg-gray-50"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3">
                <h4 class="text-lg font-medium text-gray-900">{{ config.config_name }}</h4>
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  config.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                ]">
                  {{ config.is_active ? 'Active' : 'Inactive' }}
                </span>
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  config.email_enabled ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                ]">
                  {{ config.email_enabled ? 'Email Enabled' : 'Email Disabled' }}
                </span>
              </div>
              
              <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                <div>
                  <span class="font-medium">Recipients:</span>
                  {{ config.email_recipients.length }} email(s)
                </div>
                <div>
                  <span class="font-medium">Severity Threshold:</span>
                  <SeverityBadge :severity="config.severity_threshold" size="sm" />
                </div>
                <div>
                  <span class="font-medium">Rate Limit:</span>
                  {{ config.max_alerts_per_hour }}/hour
                </div>
              </div>
              
              <div v-if="config.email_recipients.length > 0" class="mt-2">
                <span class="text-sm font-medium text-gray-700">Recipients:</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span
                    v-for="email in config.email_recipients.slice(0, 3)"
                    :key="email"
                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ email }}
                  </span>
                  <span
                    v-if="config.email_recipients.length > 3"
                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    +{{ config.email_recipients.length - 3 }} more
                  </span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <button
                @click="testAlert(config.config_name)"
                :disabled="!config.email_enabled || config.email_recipients.length === 0"
                class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              >
                <Send class="w-4 h-4 mr-1" />
                Test
              </button>
              <button
                @click="editConfiguration(config)"
                class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <Edit class="w-4 h-4 mr-1" />
                Edit
              </button>
              <button
                @click="deleteConfiguration(config)"
                :disabled="config.config_name === 'default'"
                class="inline-flex items-center px-3 py-2 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              >
                <Trash2 class="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert Configuration Modal -->
    <AlertConfigurationModal
      v-if="showCreateModal || editingConfiguration"
      :configuration="editingConfiguration"
      @close="closeModal"
      @saved="handleConfigurationSaved"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import {
  Plus, Mail, CheckCircle, XCircle, Clock, Send, Edit, Trash2
} from 'lucide-vue-next'

import SeverityBadge from '@/components/SeverityBadge.vue'
import AlertConfigurationModal from '@/components/AlertConfigurationModal.vue'
import api from '@/services/api'

export default {
  name: 'AlertsView',
  components: {
    SeverityBadge,
    AlertConfigurationModal,
    Plus,
    Mail,
    CheckCircle,
    XCircle,
    Clock,
    Send,
    Edit,
    Trash2
  },
  setup() {
    const toast = useToast()
    const loading = ref(false)
    const configurations = ref([])
    const stats = ref(null)
    const showCreateModal = ref(false)
    const editingConfiguration = ref(null)

    const fetchConfigurations = async () => {
      loading.value = true
      try {
        const response = await api.get('/alerts/configurations')
        configurations.value = response.data
      } catch (error) {
        toast.error('Failed to fetch alert configurations')
      } finally {
        loading.value = false
      }
    }

    const fetchStats = async () => {
      try {
        const response = await api.get('/alerts/stats')
        stats.value = response.data
      } catch (error) {
        console.error('Failed to fetch alert stats:', error)
      }
    }

    const testAlert = async (configName) => {
      try {
        await api.post(`/alerts/test/${configName}`)
        toast.success('Test alert sent! Check your email.')
      } catch (error) {
        toast.error('Failed to send test alert')
      }
    }

    const editConfiguration = (config) => {
      editingConfiguration.value = config
    }

    const deleteConfiguration = async (config) => {
      if (config.config_name === 'default') {
        toast.warning('Cannot delete the default configuration')
        return
      }

      if (confirm(`Are you sure you want to delete the "${config.config_name}" configuration?`)) {
        try {
          await api.delete(`/alerts/configurations/${config.id}`)
          toast.success('Configuration deleted successfully')
          await fetchConfigurations()
        } catch (error) {
          toast.error('Failed to delete configuration')
        }
      }
    }

    const closeModal = () => {
      showCreateModal.value = false
      editingConfiguration.value = null
    }

    const handleConfigurationSaved = async () => {
      await fetchConfigurations()
      closeModal()
    }

    onMounted(async () => {
      await Promise.all([
        fetchConfigurations(),
        fetchStats()
      ])
    })

    return {
      loading,
      configurations,
      stats,
      showCreateModal,
      editingConfiguration,
      testAlert,
      editConfiguration,
      deleteConfiguration,
      closeModal,
      handleConfigurationSaved
    }
  }
}
</script>
