import api from "./api"

export const huntPlaybooksService = {
  // List playbooks with optional filtering
  async listPlaybooks(filters = {}) {
    const params = new URLSearchParams()

    if (filters.category) params.append("category", filters.category)
    if (filters.severity) params.append("severity", filters.severity)
    if (filters.tags) params.append("tags", filters.tags.join(","))

    const response = await api.get(`/hunt-playbooks/playbooks?${params}`)
    return response.data
  },

  // Get detailed playbook information
  async getPlaybook(playbookId) {
    const response = await api.get(`/hunt-playbooks/playbooks/${playbookId}`)
    return response.data
  },

  // Execute a playbook
  async executePlaybook(playbookId, parameters = {}) {
    const response = await api.post(`/hunt-playbooks/playbooks/${playbookId}/execute`, {
      playbook_id: playbookId,
      parameters,
      notify_on_completion: false,
    })
    return response.data
  },

  // Create a custom playbook
  async createPlaybook(playbookData) {
    const response = await api.post("/hunt-playbooks/playbooks", playbookData)
    return response.data
  },

  // Update an existing playbook
  async updatePlaybook(playbookId, updates) {
    const response = await api.put(`/hunt-playbooks/playbooks/${playbookId}`, updates)
    return response.data
  },

  // Delete a playbook
  async deletePlaybook(playbookId) {
    const response = await api.delete(`/hunt-playbooks/playbooks/${playbookId}`)
    return response.data
  },

  // Export playbook to JSON
  async exportPlaybook(playbookId) {
    const response = await api.get(`/hunt-playbooks/playbooks/${playbookId}/export`)
    return response.data
  },

  // Import playbook from JSON
  async importPlaybook(playbookData) {
    const response = await api.post("/hunt-playbooks/playbooks/import", playbookData)
    return response.data
  },

  // Get available categories
  async getCategories() {
    const response = await api.get("/hunt-playbooks/playbooks/categories")
    return response.data
  },

  // Get available severity levels
  async getSeverities() {
    const response = await api.get("/hunt-playbooks/playbooks/severities")
    return response.data
  },

  // Get playbook templates
  async getTemplates() {
    const response = await api.get("/hunt-playbooks/playbooks/templates")
    return response.data
  },

  // Validate playbook configuration
  async validatePlaybook(playbookId) {
    const response = await api.post(`/hunt-playbooks/playbooks/${playbookId}/validate`)
    return response.data
  },

  // Get execution history
  async getExecutions(filters = {}) {
    const params = new URLSearchParams()

    if (filters.limit) params.append("limit", filters.limit)
    if (filters.offset) params.append("offset", filters.offset)
    if (filters.playbook_id) params.append("playbook_id", filters.playbook_id)
    if (filters.status) params.append("status", filters.status)

    const response = await api.get(`/hunt-playbooks/playbooks/executions?${params}`)
    return response.data
  },

  // Get specific execution details
  async getExecution(executionId) {
    const response = await api.get(`/hunt-playbooks/playbooks/executions/${executionId}`)
    return response.data
  },
}

export default huntPlaybooksService
