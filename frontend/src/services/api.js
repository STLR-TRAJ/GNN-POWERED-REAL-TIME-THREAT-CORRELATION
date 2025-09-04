"use client"

import axios from "axios"
import { useToast } from "vue-toastification"

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer dev-api-key", // In production, this should be configurable
  },
})

const toast = useToast()

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching
    config.params = {
      ...config.params,
      _t: Date.now(),
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || "An error occurred"

    // Don't show toast for certain endpoints
    const silentEndpoints = ["/dashboard/health-status"]
    const isSilent = silentEndpoints.some((endpoint) => error.config?.url?.includes(endpoint))

    if (!isSilent) {
      toast.error(message)
    }

    return Promise.reject(error)
  },
)

// API methods
export const dashboardAPI = {
  getSummary: () => api.get("/dashboard/summary"),
  getRecentActivity: (hours = 24) => api.get(`/dashboard/recent-activity?hours=${hours}`),
  getTopIndicators: (type = "ip", limit = 10) => api.get(`/dashboard/top-indicators?type=${type}&limit=${limit}`),
  getHealthStatus: () => api.get("/dashboard/health-status"),
  sendTestAlert: () => api.post("/dashboard/test-alert"),
}

export const threatsAPI = {
  getThreats: (params = {}) => api.get("/threats/", { params }),
  getThreat: (id) => api.get(`/threats/${id}`),
  searchThreats: (query, limit = 50) => api.get(`/threats/search/?q=${encodeURIComponent(query)}&limit=${limit}`),
  checkThreats: (indicators) => api.post("/threats/check", { indicators }),
  getStats: () => api.get("/threats/stats/"),
  getCriticalThreats: (limit = 10) => api.get(`/threats/critical/?limit=${limit}`),
  analyzeIndicator: (indicator, type) => api.post(`/threats/analyze/${encodeURIComponent(indicator)}?type=${type}`),
}

export default api
