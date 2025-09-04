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
              <div class="flex items-center space-x-3 mb-3">
                <SeverityBadge :severity="threat.severity" size="lg" />
                <TypeBadge :type="threat.type" />
              </div>
              <h3 class="text-lg font-medium text-gray-900 font-mono break-all">
                {{ threat.value }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                First seen {{ formatDate(threat.first_seen) }} • Last seen {{ formatDate(threat.last_seen) }}
              </p>
            </div>

            <!-- Details Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-2">Threat Information</h4>
                <dl class="space-y-2">
                  <div>
                    <dt class="text-xs text-gray-500">Source</dt>
                    <dd class="text-sm text-gray-900">{{ threat.source }}</dd>
                  </div>
                  <div>
                    <dt class="text-xs text-gray-500">Confidence</dt>
                    <dd class="text-sm text-gray-900">
                      <div class="flex items-center space-x-2">
                        <span>{{ threat.confidence }}%</span>
                        <div class="flex-1 bg-gray-200 rounded-full h-2 max-w-20">
                          <div
                            class="bg-blue-600 h-2 rounded-full"
                            :style="{ width: `${threat.confidence}%` }"
                          ></div>
                        </div>
                      </div>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs text-gray-500">Status</dt>
                    <dd class="text-sm">
                      <span :class="[
                        'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium',
                        threat.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      ]">
                        {{ threat.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </dd>
                  </div>
                </dl>
              </div>

              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-2">Timeline</h4>
                <dl class="space-y-2">
                  <div>
                    <dt class="text-xs text-gray-500">Created</dt>
                    <dd class="text-sm text-gray-900">{{ formatDate(threat.created_at) }}</dd>
                  </div>
                  <div>
                    <dt class="text-xs text-gray-500">Updated</dt>
                    <dd class="text-sm text-gray-900">{{ formatDate(threat.updated_at) }}</dd>
                  </div>
                  <div>
                    <dt class="text-xs text-gray-500">Age</dt>
                    <dd class="text-sm text-gray-900">{{ formatTimeAgo(threat.first_seen) }}</dd>
                  </div>
                </dl>
              </div>
            </div>

            <!-- Description -->
            <div v-if="threat.description" class="mb-6">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Description</h4>
              <p class="text-sm text-gray-700 bg-gray-50 p-3 rounded-md">
                {{ threat.description }}
              </p>
            </div>

            <!-- Tags -->
            <div v-if="threat.tags && threat.tags.length > 0" class="mb-6">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Tags</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in threat.tags"
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- References -->
            <div v-if="threat.references && threat.references.length > 0" class="mb-6">
              <h4 class="text-sm font-medium text-gray-900 mb-2">References</h4>
              <ul class="space-y-1">
                <li v-for="(ref, index) in threat.references" :key="index">
                  <a
                    :href="ref"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-sm text-blue-600 hover:text-blue-800 break-all"
                  >
                    {{ ref }}
                    <ExternalLink class="inline w-3 h-3 ml-1" />
                  </a>
                </li>
              </ul>
            </div>

            <!-- Recommended Actions -->
            <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
              <div class="flex">
                <AlertTriangle class="h-5 w-5 text-yellow-400" />
                <div class="ml-3">
                  <h4 class="text-sm font-medium text-yellow-800">Recommended Action</h4>
                  <p class="text-sm text-yellow-700 mt-1">
                    {{ getRecommendedAction(threat.type, threat.severity) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="$emit('close')"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Close
          </button>
          <button
            @click="analyzeIndicator"
            :disabled="analyzing"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            <Search :class="['w-4 h-4 mr-2', analyzing && 'animate-spin']" />
            {{ analyzing ? 'Analyzing...' : 'Deep Analysis' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { format, formatDistanceToNow } from 'date-fns'
import { useToast } from 'vue-toastification'
import { X, ExternalLink, AlertTriangle, Search } from 'lucide-vue-next'
import { useThreatsStore } from '@/stores/threats'

import SeverityBadge from './SeverityBadge.vue'
import TypeBadge from './TypeBadge.vue'

export default {
  name: 'ThreatDetailModal',
  components: {
    SeverityBadge,
    TypeBadge,
    X,
    ExternalLink,
    AlertTriangle,
    Search
  },
  props: {
    threat: {
      type: Object,
      required: true
    }
  },
  emits: ['close'],
  setup(props) {
    const threatsStore = useThreatsStore()
    const toast = useToast()
    const analyzing = ref(false)

    const formatDate = (dateString) => {
      return format(new Date(dateString), 'PPpp')
    }

    const formatTimeAgo = (dateString) => {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true })
    }

    const getRecommendedAction = (type, severity) => {
      const actions = {
        ip: {
          Critical: "IMMEDIATE ACTION: Block this IP address at your firewall and investigate any recent connections.",
          High: "Block this IP address at your firewall and review recent network logs.",
          Medium: "Consider blocking this IP address and monitor for suspicious activity.",
          Low: "Monitor this IP address for suspicious activity."
        },
        domain: {
          Critical: "IMMEDIATE ACTION: Block this domain at DNS level and investigate any recent connections.",
          High: "Block this domain at DNS level and review recent web traffic logs.",
          Medium: "Consider blocking this domain and monitor web traffic.",
          Low: "Monitor this domain for suspicious activity."
        },
        url: {
          Critical: "IMMEDIATE ACTION: Block this URL and scan all systems that may have accessed it.",
          High: "Block this URL at web proxy/firewall and investigate recent access.",
          Medium: "Consider blocking this URL and monitor web traffic.",
          Low: "Monitor this URL for suspicious activity."
        },
        file_hash: {
          Critical: "IMMEDIATE ACTION: Scan all systems for this malware hash and isolate infected machines.",
          High: "Scan systems for this malware hash and update antivirus signatures.",
          Medium: "Update antivirus signatures and perform system scans.",
          Low: "Update antivirus signatures and monitor for this hash."
        },
        cve: {
          Critical: "IMMEDIATE ACTION: Check if this vulnerability affects your systems and apply patches urgently.",
          High: "Review this vulnerability and prioritize patching if systems are affected.",
          Medium: "Assess impact of this vulnerability and plan patching.",
          Low: "Monitor this vulnerability for exploitation attempts."
        }
      }

      return actions[type]?.[severity] || "Review this threat and take appropriate action based on your security policies."
    }

    const analyzeIndicator = async () => {
      analyzing.value = true
      try {
        const analysis = await threatsStore.analyzeIndicator(props.threat.value, props.threat.type)
        toast.success('Analysis completed')
        console.log('Analysis result:', analysis)
        // You could emit this data or show it in a separate modal
      } catch (error) {
        toast.error('Analysis failed')
      } finally {
        analyzing.value = false
      }
    }

    return {
      analyzing,
      formatDate,
      formatTimeAgo,
      getRecommendedAction,
      analyzeIndicator
    }
  }
}
</script>
