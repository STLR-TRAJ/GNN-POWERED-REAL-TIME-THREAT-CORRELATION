import { defineStore } from "pinia"
import { dashboardAPI } from "@/services/api"

export const useDashboardStore = defineStore("dashboard", {
  state: () => ({
    summary: null,
    recentActivity: null,
    topIndicators: {},
    healthStatus: null,
    loading: false,
    error: null,
    lastUpdated: null,
  }),

  getters: {
    isHealthy: (state) => {
      return state.healthStatus?.overall_status === "healthy"
    },

    criticalThreatsCount: (state) => {
      return state.summary?.summary?.critical_alerts || 0
    },

    threatTrend: (state) => {
      const trend = state.summary?.summary?.threat_trend_24h || 0
      return {
        value: Math.abs(trend),
        direction: trend >= 0 ? "up" : "down",
        isPositive: trend <= 0, // Lower threat count is positive
      }
    },
  },

  actions: {
    async fetchSummary() {
      this.loading = true
      this.error = null

      try {
        const response = await dashboardAPI.getSummary()
        this.summary = response.data
        this.lastUpdated = new Date()
      } catch (error) {
        this.error = error.message
        console.error("Error fetching dashboard summary:", error)
      } finally {
        this.loading = false
      }
    },

    async fetchRecentActivity(hours = 24) {
      try {
        const response = await dashboardAPI.getRecentActivity(hours)
        this.recentActivity = response.data
      } catch (error) {
        console.error("Error fetching recent activity:", error)
      }
    },

    async fetchTopIndicators(type = "ip", limit = 10) {
      try {
        const response = await dashboardAPI.getTopIndicators(type, limit)
        this.topIndicators[type] = response.data
      } catch (error) {
        console.error(`Error fetching top ${type} indicators:`, error)
      }
    },

    async fetchHealthStatus() {
      try {
        const response = await dashboardAPI.getHealthStatus()
        this.healthStatus = response.data
      } catch (error) {
        console.error("Error fetching health status:", error)
        // Set unhealthy status on error
        this.healthStatus = {
          overall_status: "unhealthy",
          components: {
            database: "unknown",
            threat_feeds: "unknown",
            api: "unhealthy",
          },
        }
      }
    },

    async sendTestAlert() {
      try {
        const response = await dashboardAPI.sendTestAlert()
        return response.data
      } catch (error) {
        console.error("Error sending test alert:", error)
        throw error
      }
    },

    async refreshAll() {
      await Promise.all([
        this.fetchSummary(),
        this.fetchRecentActivity(),
        this.fetchTopIndicators("ip"),
        this.fetchTopIndicators("domain"),
        this.fetchHealthStatus(),
      ])
    },
  },
})
