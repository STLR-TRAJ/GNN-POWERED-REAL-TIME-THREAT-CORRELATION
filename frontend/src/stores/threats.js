import { defineStore } from "pinia"
import { threatsAPI } from "@/services/api"

export const useThreatsStore = defineStore("threats", {
  state: () => ({
    threats: [],
    currentThreat: null,
    searchResults: null,
    checkResults: null,
    stats: null,
    criticalThreats: [],
    loading: false,
    error: null,
    pagination: {
      page: 1,
      limit: 50,
      total: 0,
    },
    filters: {
      severity: null,
      type: null,
      source: null,
      activeOnly: true,
    },
  }),

  getters: {
    filteredThreats: (state) => {
      return state.threats.filter((threat) => {
        if (state.filters.severity && threat.severity !== state.filters.severity) return false
        if (state.filters.type && threat.type !== state.filters.type) return false
        if (state.filters.source && threat.source !== state.filters.source) return false
        if (state.filters.activeOnly && !threat.is_active) return false
        return true
      })
    },

    severityDistribution: (state) => {
      if (!state.stats?.threats_by_severity) return {}
      return state.stats.threats_by_severity
    },

    typeDistribution: (state) => {
      if (!state.stats?.threats_by_type) return {}
      return state.stats.threats_by_type
    },
  },

  actions: {
    async fetchThreats(params = {}) {
      this.loading = true
      this.error = null

      try {
        const queryParams = {
          skip: (this.pagination.page - 1) * this.pagination.limit,
          limit: this.pagination.limit,
          ...this.filters,
          ...params,
        }

        const response = await threatsAPI.getThreats(queryParams)
        this.threats = response.data

        // Update pagination if total is provided in headers
        const total = response.headers["x-total-count"]
        if (total) {
          this.pagination.total = Number.parseInt(total)
        }
      } catch (error) {
        this.error = error.message
        console.error("Error fetching threats:", error)
      } finally {
        this.loading = false
      }
    },

    async fetchThreat(id) {
      this.loading = true
      this.error = null

      try {
        const response = await threatsAPI.getThreat(id)
        this.currentThreat = response.data
      } catch (error) {
        this.error = error.message
        console.error("Error fetching threat:", error)
      } finally {
        this.loading = false
      }
    },

    async searchThreats(query, limit = 50) {
      this.loading = true
      this.error = null

      try {
        const response = await threatsAPI.searchThreats(query, limit)
        this.searchResults = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error("Error searching threats:", error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async checkIndicators(indicators) {
      this.loading = true
      this.error = null

      try {
        const response = await threatsAPI.checkThreats(indicators)
        this.checkResults = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error("Error checking indicators:", error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchStats() {
      try {
        const response = await threatsAPI.getStats()
        this.stats = response.data
      } catch (error) {
        console.error("Error fetching threat stats:", error)
      }
    },

    async fetchCriticalThreats(limit = 10) {
      try {
        const response = await threatsAPI.getCriticalThreats(limit)
        this.criticalThreats = response.data
      } catch (error) {
        console.error("Error fetching critical threats:", error)
      }
    },

    async analyzeIndicator(indicator, type) {
      this.loading = true
      this.error = null

      try {
        const response = await threatsAPI.analyzeIndicator(indicator, type)
        return response.data
      } catch (error) {
        this.error = error.message
        console.error("Error analyzing indicator:", error)
        throw error
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1 // Reset to first page when filters change
    },

    setPage(page) {
      this.pagination.page = page
    },

    clearSearch() {
      this.searchResults = null
    },

    clearCheck() {
      this.checkResults = null
    },
  },
})
