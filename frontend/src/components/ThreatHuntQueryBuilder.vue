<template>
  <div class="query-builder">
    <div class="space-y-6">
      <!-- Filters Section -->
      <div>
        <h3 class="text-sm font-medium text-gray-900 mb-3">Filters</h3>
        <div class="space-y-3">
          <div
            v-for="(filter, index) in filters"
            :key="index"
            class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
          >
            <select
              v-model="filter.field"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Field</option>
              <option value="value">Indicator Value</option>
              <option value="type">Type</option>
              <option value="severity">Severity</option>
              <option value="confidence">Confidence</option>
              <option value="source">Source</option>
              <option value="malware_family">Malware Family</option>
              <option value="first_seen">First Seen</option>
              <option value="last_seen">Last Seen</option>
              <option value="threat_score">Threat Score</option>
            </select>
            
            <select
              v-model="filter.operator"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="eq">Equals</option>
              <option value="ne">Not Equals</option>
              <option value="gt">Greater Than</option>
              <option value="gte">Greater Than or Equal</option>
              <option value="lt">Less Than</option>
              <option value="lte">Less Than or Equal</option>
              <option value="like">Contains</option>
              <option value="in">In List</option>
            </select>
            
            <input
              v-if="!isMultiValue(filter.operator)"
              v-model="filter.value"
              :type="getInputType(filter.field)"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :placeholder="getPlaceholder(filter.field)"
            />
            
            <textarea
              v-else
              v-model="filter.valueText"
              @input="updateMultiValue(filter)"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter values separated by commas"
              rows="2"
            ></textarea>
            
            <button
              @click="removeFilter(index)"
              class="text-red-600 hover:text-red-800"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
          
          <button
            @click="addFilter"
            class="flex items-center space-x-2 text-blue-600 hover:text-blue-800"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>Add Filter</span>
          </button>
        </div>
      </div>

      <!-- Sorting Section -->
      <div>
        <h3 class="text-sm font-medium text-gray-900 mb-3">Sorting</h3>
        <div class="flex items-center space-x-3">
          <select
            v-model="sortField"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">No Sorting</option>
            <option value="last_seen">Last Seen</option>
            <option value="first_seen">First Seen</option>
            <option value="threat_score">Threat Score</option>
            <option value="confidence">Confidence</option>
            <option value="severity">Severity</option>
          </select>
          
          <select
            v-model="sortOrder"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>
      </div>

      <!-- Limits Section -->
      <div>
        <h3 class="text-sm font-medium text-gray-900 mb-3">Limits</h3>
        <div class="flex items-center space-x-3">
          <label class="text-sm text-gray-600">Limit:</label>
          <input
            v-model.number="limit"
            type="number"
            min="1"
            max="5000"
            class="w-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <label class="text-sm text-gray-600">Offset:</label>
          <input
            v-model.number="offset"
            type="number"
            min="0"
            class="w-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between pt-4 border-t border-gray-200">
        <div class="flex space-x-3">
          <button
            @click="executeQuery"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Execute Query
          </button>
          <button
            @click="saveQuery"
            class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
          >
            Save Query
          </button>
        </div>
        
        <button
          @click="clearQuery"
          class="text-gray-600 hover:text-gray-800"
        >
          Clear All
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, computed } from 'vue'

export default {
  name: 'ThreatHuntQueryBuilder',
  props: {
    modelValue: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['update:modelValue', 'execute', 'save'],
  setup(props, { emit }) {
    const filters = ref([])
    const sortField = ref('')
    const sortOrder = ref('desc')
    const limit = ref(1000)
    const offset = ref(0)

    const addFilter = () => {
      filters.value.push({
        field: '',
        operator: 'eq',
        value: '',
        valueText: ''
      })
    }

    const removeFilter = (index) => {
      filters.value.splice(index, 1)
    }

    const isMultiValue = (operator) => {
      return operator === 'in'
    }

    const updateMultiValue = (filter) => {
      if (filter.valueText) {
        filter.value = filter.valueText.split(',').map(v => v.trim()).filter(v => v)
      }
    }

    const getInputType = (field) => {
      if (['first_seen', 'last_seen'].includes(field)) {
        return 'datetime-local'
      }
      if (['confidence', 'threat_score'].includes(field)) {
        return 'number'
      }
      return 'text'
    }

    const getPlaceholder = (field) => {
      const placeholders = {
        value: 'Enter indicator value',
        type: 'ip, domain, file_hash, url',
        severity: 'Low, Medium, High, Critical',
        confidence: '0-100',
        source: 'Source name',
        malware_family: 'Malware family name',
        threat_score: '0-100'
      }
      return placeholders[field] || 'Enter value'
    }

    const buildQuery = () => {
      const query = {
        filters: {},
        limit: limit.value,
        offset: offset.value
      }

      // Build filters
      filters.value.forEach(filter => {
        if (filter.field && filter.operator && (filter.value || filter.value === 0)) {
          query.filters[filter.field] = {
            operator: filter.operator,
            value: filter.value
          }
        }
      })

      // Add sorting
      if (sortField.value) {
        query.sort = {
          field: sortField.value,
          order: sortOrder.value
        }
      }

      return query
    }

    const executeQuery = () => {
      const query = buildQuery()
      emit('execute', query)
      emit('update:modelValue', query)
    }

    const saveQuery = () => {
      const query = buildQuery()
      emit('save', query)
      emit('update:modelValue', query)
    }

    const clearQuery = () => {
      filters.value = []
      sortField.value = ''
      sortOrder.value = 'desc'
      limit.value = 1000
      offset.value = 0
      emit('update:modelValue', {})
    }

    // Load initial query
    watch(() => props.modelValue, (newQuery) => {
      if (newQuery && Object.keys(newQuery).length > 0) {
        // Load filters
        filters.value = []
        if (newQuery.filters) {
          Object.entries(newQuery.filters).forEach(([field, filterSpec]) => {
            const filter = {
              field,
              operator: filterSpec.operator,
              value: filterSpec.value,
              valueText: Array.isArray(filterSpec.value) ? filterSpec.value.join(', ') : ''
            }
            filters.value.push(filter)
          })
        }

        // Load sorting
        if (newQuery.sort) {
          sortField.value = newQuery.sort.field
          sortOrder.value = newQuery.sort.order
        }

        // Load limits
        if (newQuery.limit) limit.value = newQuery.limit
        if (newQuery.offset) offset.value = newQuery.offset
      }
    }, { immediate: true })

    return {
      filters,
      sortField,
      sortOrder,
      limit,
      offset,
      addFilter,
      removeFilter,
      isMultiValue,
      updateMultiValue,
      getInputType,
      getPlaceholder,
      executeQuery,
      saveQuery,
      clearQuery
    }
  }
}
</script>
