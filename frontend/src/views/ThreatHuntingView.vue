<template>
  <div class="threat-hunting-view">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Threat Hunting</h1>
          <p class="text-sm text-gray-600 mt-1">Proactive threat detection and investigation</p>
        </div>
        <div class="flex space-x-3">
          <button
            @click="showTemplates = true"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <i class="fas fa-template mr-2"></i>
            Templates
          </button>
          <button
            @click="exportResults"
            :disabled="!huntResults.length"
            class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
          >
            <i class="fas fa-download mr-2"></i>
            Export
          </button>
        </div>
      </div>
    </div>

    <div class="flex h-full">
      <!-- Query Builder Sidebar -->
      <div class="w-1/3 bg-gray-50 border-r border-gray-200 p-6">
        <ThreatHuntQueryBuilder
          @query-built="executeHunt"
          @pivot-request="executePivot"
          :loading="loading"
        />
      </div>

      <!-- Results Panel -->
      <div class="flex-1 p-6">
        <!-- Hunt Results -->
        <div v-if="huntResults.length" class="mb-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-semibold text-gray-900">Hunt Results</h2>
                <div class="flex items-center space-x-4 text-sm text-gray-600">
                  <span>{{ huntResults.length }} results</span>
                  <span v-if="huntAnalytics">
                    Execution time: {{ formatExecutionTime(huntAnalytics.execution_time) }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Results Table -->
            <div class="overflow-x-auto">
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
                  <tr v-for="result in huntResults" :key="result.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ result.value }}</div>
                      <div class="text-sm text-gray-500">{{ result.source }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <TypeBadge :type="result.type" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SeverityBadge :severity="result.severity" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-16 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            class="bg-blue-600 h-2 rounded-full" 
                            :style="{ width: result.confidence + '%' }"
                          ></div>
                        </div>
                        <span class="text-sm text-gray-600">{{ result.confidence }}%</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(result.last_seen) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        @click="pivotOnIndicator(result)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Pivot
                      </button>
                      <button
                        @click="viewDetails(result)"
                        class="text-green-600 hover:text-green-900"
                      >
                        Details
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Analytics Panel -->
        <div v-if="huntAnalytics" class="mb-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Hunt Analytics</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <!-- Threat Distribution -->
              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="text-sm font-medium text-gray-700 mb-2">By Severity</h4>
                <div class="space-y-2">
                  <div v-for="(count, severity) in huntAnalytics.threat_distribution.by_severity" :key="severity" class="flex justify-between">
                    <span class="text-sm text-gray-600">{{ severity }}</span>
                    <span class="text-sm font-medium">{{ count }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="text-sm font-medium text-gray-700 mb-2">By Type</h4>
                <div class="space-y-2">
                  <div v-for="(count, type) in huntAnalytics.threat_distribution.by_type" :key="type" class="flex justify-between">
                    <span class="text-sm text-gray-600">{{ type }}</span>
                    <span class="text-sm font-medium">{{ count }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="text-sm font-medium text-gray-700 mb-2">Confidence</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Average</span>
                    <span class="text-sm font-medium">{{ Math.round(huntAnalytics.confidence_analysis.average_confidence) }}%</span>
                  </div>
                  <div v-for="(count, level) in huntAnalytics.confidence_analysis.confidence_distribution" :key="level" class="flex justify-between">
                    <span class="text-sm text-gray-600">{{ level }}</span>
                    <span class="text-sm font-medium">{{ count }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="text-sm font-medium text-gray-700 mb-2">Threat Score</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Average</span>
                    <span class="text-sm font-medium">{{ Math.round(huntAnalytics.threat_score_analysis.average_threat_score) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">High Risk</span>
                    <span class="text-sm font-medium">{{ huntAnalytics.threat_score_analysis.high_risk_count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pivot Results -->
        <div v-if="pivotResults" class="mb-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">
              Pivot Analysis: {{ pivotResults.pivot_type }} - {{ pivotResults.pivot_value }}
            </h3>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Related Indicators -->
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">Related Indicators</h4>
                <div class="space-y-2 max-h-64 overflow-y-auto">
                  <div v-for="indicator in pivotResults.related_indicators" :key="indicator.id" 
                       class="flex items-center justify-between p-2 bg-gray-50 rounded">
                    <div>
                      <span class="text-sm font-medium">{{ indicator.value }}</span>
                      <span class="text-xs text-gray-500 ml-2">{{ indicator.type }}</span>
                    </div>
                    <SeverityBadge :severity="indicator.severity" size="sm" />
                  </div>
                </div>
              </div>

              <!-- Analysis Summary -->
              <div>
                <h4 class="text-md font-medium text-gray-700 mb-3">Analysis Summary</h4>
                <div class="space-y-3">
                  <div v-if="pivotResults.network_analysis" class="bg-blue-50 p-3 rounded">
                    <h5 class="text-sm font-medium text-blue-900">Network Analysis</h5>
                    <p class="text-sm text-blue-700">
                      Subnet: {{ pivotResults.network_analysis.subnet }}
                    </p>
                    <p class="text-sm text-blue-700">
                      Related IPs: {{ pivotResults.network_analysis.related_ips_count }}
                    </p>
                  </div>
                  
                  <div v-if="pivotResults.domain_analysis" class="bg-green-50 p-3 rounded">
                    <h5 class="text-sm font-medium text-green-900">Domain Analysis</h5>
                    <p class="text-sm text-green-700">
                      Related domains: {{ pivotResults.domain_analysis.related_domains_count }}
                    </p>
                  </div>
                  
                  <div v-if="pivotResults.malware_analysis" class="bg-red-50 p-3 rounded">
                    <h5 class="text-sm font-medium text-red-900">Malware Analysis</h5>
                    <p class="text-sm text-red-700">
                      Family: {{ pivotResults.malware_analysis.malware_family }}
                    </p>
                    <p class="text-sm text-red-700">
                      Samples: {{ pivotResults.malware_analysis.family_samples_count }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Timeline Visualization -->
        <div v-if="timelineData" class="mb-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Timeline Analysis</h3>
            <ThreatTimeline :timeline-data="timelineData" />
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!huntResults.length && !loading" class="text-center py-12">
          <div class="mx-auto h-12 w-12 text-gray-400">
            <i class="fas fa-search text-4xl"></i>
          </div>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No hunt results</h3>
          <p class="mt-1 text-sm text-gray-500">Build a query to start threat hunting</p>
        </div>
      </div>
    </div>

    <!-- Templates Modal -->
    <div v-if="showTemplates" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Hunt Templates</h3>
          <button @click="showTemplates = false" class="text-gray-400 hover:text-gray-600">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="space-y-3 max-h-96 overflow-y-auto">
          <div v-for="template in huntTemplates" :key="template.name" 
               class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
               @click="useTemplate(template)">
            <h4 class="font-medium text-gray-900">{{ template.name }}</h4>
            <p class="text-sm text-gray-600 mt-1">{{ template.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 shadow-lg">
        <div class="flex items-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
          <span class="text-gray-700">{{ loadingMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import ThreatHuntQueryBuilder from '@/components/ThreatHuntQueryBuilder.vue'
import ThreatTimeline from '@/components/ThreatTimeline.vue'
import SeverityBadge from '@/components/SeverityBadge.vue'
import TypeBadge from '@/components/TypeBadge.vue'
import { threatHuntingService } from '@/services/threatHunting'

export default {
  name: 'ThreatHuntingView',
  components: {
    ThreatHuntQueryBuilder,
    ThreatTimeline,
    SeverityBadge,
    TypeBadge
  },
  setup() {
    const huntResults = ref([])
    const huntAnalytics = ref(null)
    const pivotResults = ref(null)
    const timelineData = ref(null)
    const huntTemplates = ref([])
    const loading = ref(false)
    const loadingMessage = ref('')
    const showTemplates = ref(false)

    const executeHunt = async (query) => {
      loading.value = true
      loadingMessage.value = 'Executing hunt query...'
      
      try {
        const response = await threatHuntingService.executeQuery(query)
        huntResults.value = response.results
        huntAnalytics.value = response.analytics
      } catch (error) {
        console.error('Hunt execution failed:', error)
        // Handle error
      } finally {
        loading.value = false
      }
    }

    const executePivot = async (pivotRequest) => {
      loading.value = true
      loadingMessage.value = 'Performing pivot analysis...'
      
      try {
        const response = await threatHuntingService.pivotAnalysis(pivotRequest)
        pivotResults.value = response
      } catch (error) {
        console.error('Pivot analysis failed:', error)
      } finally {
        loading.value = false
      }
    }

    const pivotOnIndicator = (indicator) => {
      const pivotType = indicator.type === 'ip' ? 'ip' : 
                       indicator.type === 'domain' ? 'domain' :
                       indicator.type === 'file_hash' ? 'hash' : 'domain'
      
      executePivot({
        pivot_type: pivotType,
        pivot_value: indicator.value,
        depth: 2
      })
    }

    const viewDetails = (indicator) => {
      // Open detailed view modal
      console.log('View details for:', indicator)
    }

    const exportResults = () => {
      if (!huntResults.value.length) return
      
      const csv = [
        ['Indicator', 'Type', 'Severity', 'Confidence', 'Threat Score', 'Source', 'Last Seen'].join(','),
        ...huntResults.value.map(result => [
          result.value,
          result.type,
          result.severity,
          result.confidence,
          result.threat_score,
          result.source,
          result.last_seen
        ].join(','))
      ].join('\n')
      
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `hunt-results-${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    }

    const useTemplate = (template) => {
      showTemplates.value = false
      executeHunt(template.query)
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const formatExecutionTime = (timestamp) => {
      const now = new Date()
      const execTime = new Date(timestamp)
      const diff = now - execTime
      return `${Math.round(diff / 1000)}s ago`
    }

    const loadTemplates = async () => {
      try {
        const templates = await threatHuntingService.getTemplates()
        huntTemplates.value = templates
      } catch (error) {
        console.error('Failed to load templates:', error)
      }
    }

    onMounted(() => {
      loadTemplates()
    })

    return {
      huntResults,
      huntAnalytics,
      pivotResults,
      timelineData,
      huntTemplates,
      loading,
      loadingMessage,
      showTemplates,
      executeHunt,
      executePivot,
      pivotOnIndicator,
      viewDetails,
      exportResults,
      useTemplate,
      formatDate,
      formatExecutionTime
    }
  }
}
</script>

<style scoped>
.threat-hunting-view {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}
</style>
