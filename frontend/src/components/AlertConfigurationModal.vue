<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            @click="$emit('close')"
            class="bg-white rounded-md text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <X class="h-6 w-6" />
          </button>
        </div>

        <div class="sm:flex sm:items-start">
          <div class="w-full">
            <!-- Header -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900">
                {{ isEditing ? 'Edit Alert Configuration' : 'Create Alert Configuration' }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                Configure email alerts and notification settings
              </p>
            </div>

            <!-- Form -->
            <form @submit.prevent="saveConfiguration" class="space-y-6">
              <!-- Configuration Name -->
              <div>
                <label for="config-name" class="block text-sm font-medium text-gray-700">
                  Configuration Name
                </label>
                <input
                  id="config-name"
                  v-model="formData.config_name"
                  type="text"
                  required
                  :disabled="isEditing"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm disabled:bg-gray-100"
                  placeholder="e.g., default, security-team, executives"
                />
              </div>

              <!-- Email Settings -->
              <div class="space-y-4">
                <h4 class="text-md font-medium text-gray-900">Email Settings</h4>
                
                <div class="flex items-center">
                  <input
                    id="email-enabled"
                    v-model="formData.email_enabled"
                    type="checkbox"
                    class="h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded"
                  />
                  <label for="email-enabled" class="ml-2 block text-sm text-gray-900">
                    Enable email alerts
                  </label>
                </div>

                <div v-if="formData.email_enabled">
                  <label for="email-recipients" class="block text-sm font-medium text-gray-700">
                    Email Recipients
                  </label>
                  <div class="mt-1">
                    <div class="flex flex-wrap gap-2 mb-2">
                      <span
                        v-for="(email, index) in formData.email_recipients"
                        :key="index"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {{ email }}
                        <button
                          type="button"
                          @click="removeEmail(index)"
                          class="ml-1 inline-flex items-center p-0.5 rounded-full text-blue-400 hover:text-blue-600"
                        >
                          <X class="h-3 w-3" />
                        </button>
                      </span>
                    </div>
                    <div class="flex">
                      <input
                        v-model="newEmail"
                        type="email"
                        placeholder="Enter email address"
                        class="flex-1 px-3 py-2 border border-gray-300 rounded-l-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                        @keyup.enter="addEmail"
                      />
                      <button
                        type="button"
                        @click="addEmail"
                        class="px-4 py-2 border border-l-0 border-gray-300 rounded-r-md bg-gray-50 text-gray-700 hover:bg-gray-100"
                      >
                        Add
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Alert Thresholds -->
              <div class="space-y-4">
                <h4 class="text-md font-medium text-gray-900">Alert Thresholds</h4>
                
                <div>
                  <label for="severity-threshold" class="block text-sm font-medium text-gray-700">
                    Minimum Severity Level
                  </label>
                  <select
                    id="severity-threshold"
                    v-model="formData.severity_threshold"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                  </select>
                  <p class="mt-1 text-xs text-gray-500">
                    Only alerts at or above this severity level will be sent
                  </p>
                </div>

                <div>
                  <label for="max-alerts" class="block text-sm font-medium text-gray-700">
                    Maximum Alerts Per Hour
                  </label>
                  <input
                    id="max-alerts"
                    v-model.number="formData.max_alerts_per_hour"
                    type="number"
                    min="1"
                    max="100"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    Prevents alert spam by limiting the number of alerts sent per hour
                  </p>
                </div>
              </div>

              <!-- SMTP Settings -->
              <div v-if="formData.email_enabled" class="space-y-4">
                <h4 class="text-md font-medium text-gray-900">SMTP Settings</h4>
                <p class="text-sm text-gray-500">
                  Leave blank to use default system settings
                </p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label for="smtp-server" class="block text-sm font-medium text-gray-700">
                      SMTP Server
                    </label>
                    <input
                      id="smtp-server"
                      v-model="formData.smtp_server"
                      type="text"
                      placeholder="smtp.gmail.com"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="smtp-port" class="block text-sm font-medium text-gray-700">
                      SMTP Port
                    </label>
                    <input
                      id="smtp-port"
                      v-model.number="formData.smtp_port"
                      type="number"
                      placeholder="587"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="smtp-username" class="block text-sm font-medium text-gray-700">
                      SMTP Username
                    </label>
                    <input
                      id="smtp-username"
                      v-model="formData.smtp_username"
                      type="text"
                      placeholder="your-email@gmail.com"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label for="smtp-password" class="block text-sm font-medium text-gray-700">
                      SMTP Password
                    </label>
                    <input
                      id="smtp-password"
                      v-model="formData.smtp_password"
                      type="password"
                      placeholder="App password or regular password"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                    />
                  </div>
                </div>

                <div class="flex items-center">
                  <input
                    id="smtp-tls"
                    v-model="formData.smtp_use_tls"
                    type="checkbox"
                    class="h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded"
                  />
                  <label for="smtp-tls" class="ml-2 block text-sm text-gray-900">
                    Use TLS encryption (recommended)
                  </label>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
                <button
                  type="button"
                  @click="$emit('close')"
                  class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  @click="testConfiguration"
                  :disabled="!formData.email_enabled || formData.email_recipients.length === 0 || testing"
                  class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                >
                  <Mail :class="['w-4 h-4 mr-2', testing && 'animate-spin']" />
                  {{ testing ? 'Testing...' : 'Test Email' }}
                </button>
                <button
                  type="submit"
                  :disabled="saving"
                  class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                >
                  <Save :class="['w-4 h-4 mr-2', saving && 'animate-spin']" />
                  {{ saving ? 'Saving...' : (isEditing ? 'Update' : 'Create') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { useToast } from 'vue-toastification'
import { X, Mail, Save } from 'lucide-vue-next'
import api from '@/services/api'

export default {
  name: 'AlertConfigurationModal',
  components: {
    X,
    Mail,
    Save
  },
  props: {
    configuration: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const toast = useToast()
    const saving = ref(false)
    const testing = ref(false)
    const newEmail = ref('')

    const formData = reactive({
      config_name: '',
      email_enabled: true,
      email_recipients: [],
      severity_threshold: 'High',
      max_alerts_per_hour: 10,
      smtp_server: '',
      smtp_port: 587,
      smtp_username: '',
      smtp_password: '',
      smtp_use_tls: true
    })

    const isEditing = computed(() => !!props.configuration)

    // Initialize form data
    watch(() => props.configuration, (config) => {
      if (config) {
        Object.assign(formData, {
          config_name: config.config_name,
          email_enabled: config.email_enabled,
          email_recipients: [...config.email_recipients],
          severity_threshold: config.severity_threshold,
          max_alerts_per_hour: config.max_alerts_per_hour,
          smtp_server: config.smtp_server || '',
          smtp_port: config.smtp_port || 587,
          smtp_username: config.smtp_username || '',
          smtp_password: '', // Don't populate password for security
          smtp_use_tls: config.smtp_use_tls
        })
      }
    }, { immediate: true })

    const addEmail = () => {
      const email = newEmail.value.trim()
      if (email && !formData.email_recipients.includes(email)) {
        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (emailRegex.test(email)) {
          formData.email_recipients.push(email)
          newEmail.value = ''
        } else {
          toast.error('Please enter a valid email address')
        }
      }
    }

    const removeEmail = (index) => {
      formData.email_recipients.splice(index, 1)
    }

    const saveConfiguration = async () => {
      saving.value = true
      try {
        const payload = { ...formData }
        
        // Remove empty SMTP fields
        if (!payload.smtp_server) delete payload.smtp_server
        if (!payload.smtp_username) delete payload.smtp_username
        if (!payload.smtp_password) delete payload.smtp_password

        let response
        if (isEditing.value) {
          response = await api.put(`/alerts/configurations/${props.configuration.id}`, payload)
        } else {
          response = await api.post('/alerts/configurations', payload)
        }

        toast.success(`Alert configuration ${isEditing.value ? 'updated' : 'created'} successfully`)
        emit('saved', response.data)
        emit('close')
      } catch (error) {
        toast.error(`Failed to ${isEditing.value ? 'update' : 'create'} configuration`)
      } finally {
        saving.value = false
      }
    }

    const testConfiguration = async () => {
      testing.value = true
      try {
        // First save the configuration if it's new
        if (!isEditing.value) {
          await saveConfiguration()
        }

        const configName = formData.config_name
        await api.post(`/alerts/test/${configName}`)
        toast.success('Test alert sent! Check your email.')
      } catch (error) {
        toast.error('Failed to send test alert')
      } finally {
        testing.value = false
      }
    }

    return {
      formData,
      newEmail,
      saving,
      testing,
      isEditing,
      addEmail,
      removeEmail,
      saveConfiguration,
      testConfiguration
    }
  }
}
</script>
