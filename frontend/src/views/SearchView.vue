<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Threat Intelligence Search</h1>
      <p class="text-gray-600">Search for specific indicators and analyze threats</p>
    </div>

    <!-- Search Form -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="space-y-4">
        <div>
          <label for="search-input" class="block text-sm font-medium text-gray-700 mb-2">
            Search for IP addresses, domains, URLs, file hashes, or CVEs
          </label>
          <div class="flex space-x-3">
            <div class="flex-1">
              <input
                id="search-input"
                v-model="searchQuery"
                @keyup.enter="performSearch"
                type="text"
                placeholder="e.g., 192.168.1.1, malicious.com, CVE-2024-1234"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
              />
            </div>
            <button
              @click="performSearch"
              :disabled="!searchQuery.trim() || loading"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              <Search :class="['w-4 h-4 mr-2', loading && 'animate-spin']" />
              Search
            </button>
          </div>
        </div>

        <!-- Bulk Check -->
        <div class="border-t pt-4">
          <label for="bulk-input" class="block text-sm font-medium text-gray-700 mb-2">
            Bulk Check (one indicator per line)
          </label>
          <div class="space-y-3">
            <textarea
              id="bulk-input"
              v-model="bulkInput"
              rows="4"
              placeholder="192.168.1.1&#10;malicious.com&#10;http://evil.example.com&#10;abc123def456..."
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
            ></textarea>
            <button
              @click="performBulkCheck"
              :disabled="!bulkInput.trim() || loading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              <CheckCircle :class="['w-4 h-4 mr-2', loading && 'animate-spin']" />
              Check All
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults" class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">Search Results</h3>
          <div class="text-sm text-gray-500">
            {{ searchResults.total_results }} results in {{ searchResults.execution_time_ms }}ms
          </div>
        </div>
      </div>
      
      <div v-if="searchResults.results.length === 0" class="p-6 text-center">
        <Search class="w-12 h-12 mx-auto mb-3 text-gray-300" />
        <p class="text-gray-500">No threats found for "{{ searchResults.query }}"</p>
        <p class="text-sm text-gray-400 mt-1">This indicator appears to be clean</p>
      </div>
      
      <div v-else class="divide-y divide-gray-200">
        <ThreatCard
          v-for="threat in searchResults.results"
          :key="threat.id"
          :threat="threat"
          @click="viewThreat(threat)"
        />
      </div>
    </div>

    <!-- Bulk Check Results -->
    <div v-if="checkResults" class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">Bulk Check Results</h3>
          <div class="text-sm text-gray-500">
            {{ checkResults.malicious_count }} of {{ checkResults.total_checked }} are malicious
          </div>
        </div>
      </div>
      
      <div class="p-6">
        <div class="space-y-3">
          <div
            v-for="result in checkResults.results"
            :key="result.indicator"
            class="flex items-center justify-between p-3 border rounded-lg"
            :class="result.is_malicious ? 'border-red-200 bg-red-50' : 'border-green-200 bg-green-50'"
          >
            <div class="flex items-center space-x-3">
              <div :class="[
                'w-3 h-3 rounded-full',
                result.is_malicious ? 'bg-red-500' : 'bg-green-500'
              ]"></div>
              <div>
                <p class="text-sm font-medium text-gray-900 font-mono">{{ result.indicator }}</p>
                <div v-if="result.is_malicious" class="flex items-center space-x-2 mt-1">
                  <SeverityBadge :severity="result.severity" size="sm" />
                  <span class="text-xs text-gray-500">{{ result.confidence }}% confidence</span>
                </div>
              </div>
            </div>
            <div class="text-right">
              <div :class="[
                'text-sm font-medium',
                result.is_malicious ? 'text-red-700' : 'text-green-700'
              ]">
                {{ result.is_malicious ? 'Malicious' : 'Clean' }}
              </div>
              <div v-if="result.sources?.length" class="text-xs text-gray-500">
                {{ result.sources.join(', ') }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Examples -->
    <div class="bg-blue-50 rounded-lg p-6">
      <h3 class="text-lg font-medium text-blue-900 mb-3">Quick Examples</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <button
          v-for="example in examples"
          :key="example.value"
          @click="searchQuery = example.value; performSearch()"
          class="text-left p-3 bg-white rounded border border-blue-200 hover:border-blue-300 transition-colors"
        >
          <div class="text-sm font-medium text-blue-900">{{ example.type }}</div>
          <div class="text-xs text-blue-600 font-mono">{{ example.value }}</div>
        </button>
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
import { ref, computed } from 'vue'
import { useThreatsStore } from '@/stores/threats'
import { useToast } from 'vue-toastification'
import { Search, CheckCircle } from 'lucide-vue-next'

import ThreatCard from '@/components/ThreatCard.vue'
import SeverityBadge from '@/components/SeverityBadge.vue'
import ThreatDetailModal from '@/components/ThreatDetailModal.vue'

export default {
  name: 'SearchView',
  components: {
    ThreatCard,
    SeverityBadge,
    ThreatDetailModal,
    Search,
    CheckCircle
  },
  setup() {
    const threatsStore = useThreatsStore()
    const toast = useToast()

    const searchQuery = ref('')
    const bulkInput = ref('')
    const selectedThreat = ref(null)

    const examples = [
      { type: 'IP Address', value: '192.168.1.100' },
      { type: 'Domain', value: 'malicious.example.com' },
      { type: 'URL', value: 'http://evil.example.com/malware' },
      { type: 'CVE', value: 'CVE-2024-1234' }
    ]

    const loading = computed(() => threatsStore.loading)
    const searchResults = computed(() => threatsStore.searchResults)
    const checkResults = computed(() => threatsStore.checkResults)

    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        toast.warning('Please enter a search query')
        return
      }

      try {
        await threatsStore.searchThreats(searchQuery.value.trim())
        
        if (searchResults.value?.total_results === 0) {
          toast.info(`No threats found for "${searchQuery.value}"`)
        } else {
          toast.success(`Found ${searchResults.value?.total_results} results`)
        }
      } catch (error) {
        toast.error('Search failed')
      }
    }

    const performBulkCheck = async () => {
      if (!bulkInput.value.trim()) {
        toast.warning('Please enter indicators to check')
        return
      }

      const indicators = bulkInput.value
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)

      if (indicators.length === 0) {
        toast.warning('No valid indicators found')
        return
      }

      if (indicators.length > 100) {
        toast.warning('Maximum 100 indicators allowed per bulk check')
        return
      }

      try {
        await threatsStore.checkIndicators(indicators)
        
        const maliciousCount = checkResults.value?.malicious_count || 0
        const totalCount = checkResults.value?.total_checked || 0
        
        if (maliciousCount === 0) {
          toast.success('All indicators appear to be clean')
        } else {
          toast.warning(`${maliciousCount} of ${totalCount} indicators are malicious`)
        }
      } catch (error) {
        toast.error('Bulk check failed')
      }
    }

    const viewThreat = (threat) => {
      selectedThreat.value = threat
    }

    return {
      searchQuery,
      bulkInput,
      selectedThreat,
      examples,
      loading,
      searchResults,
      checkResults,
      performSearch,
      performBulkCheck,
      viewThreat
    }
  }
}
</script>
