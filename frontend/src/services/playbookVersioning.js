/**
 * Playbook Versioning Service
 * Handles API calls for playbook version control and change tracking
 */

import api from "./api"

export const playbookVersioningService = {
  /**
   * Create a new version of a playbook
   */
  async createVersion(playbookId, versionData) {
    try {
      const response = await api.post(`/playbook-versioning/playbooks/${playbookId}/versions`, versionData)
      return response.data
    } catch (error) {
      console.error("Error creating version:", error)
      throw error
    }
  },

  /**
   * Get version history for a playbook
   */
  async getVersionHistory(playbookId) {
    try {
      const response = await api.get(`/playbook-versioning/playbooks/${playbookId}/versions`)
      return response.data
    } catch (error) {
      console.error("Error getting version history:", error)
      throw error
    }
  },

  /**
   * Activate a specific version
   */
  async activateVersion(versionId) {
    try {
      const response = await api.post(`/playbook-versioning/versions/${versionId}/activate`)
      return response.data
    } catch (error) {
      console.error("Error activating version:", error)
      throw error
    }
  },

  /**
   * Get diff between two versions
   */
  async getVersionDiff(versionId, compareToId = null) {
    try {
      const params = compareToId ? { compare_to_id: compareToId } : {}
      const response = await api.get(`/playbook-versioning/versions/${versionId}/diff`, { params })
      return response.data
    } catch (error) {
      console.error("Error getting version diff:", error)
      throw error
    }
  },

  /**
   * Rollback to a specific version
   */
  async rollbackToVersion(playbookId, versionId) {
    try {
      const response = await api.post(`/playbook-versioning/playbooks/${playbookId}/rollback/${versionId}`)
      return response.data
    } catch (error) {
      console.error("Error rolling back version:", error)
      throw error
    }
  },

  /**
   * Create a new branch from a version
   */
  async createBranch(playbookId, branchData) {
    try {
      const response = await api.post(`/playbook-versioning/playbooks/${playbookId}/branches`, branchData)
      return response.data
    } catch (error) {
      console.error("Error creating branch:", error)
      throw error
    }
  },

  /**
   * Merge a branch version into main line
   */
  async mergeBranch(targetVersionId, sourceVersionId) {
    try {
      const response = await api.post(`/playbook-versioning/versions/${targetVersionId}/merge/${sourceVersionId}`)
      return response.data
    } catch (error) {
      console.error("Error merging branch:", error)
      throw error
    }
  },

  /**
   * Get detailed information about a specific version
   */
  async getVersionDetails(versionId) {
    try {
      const response = await api.get(`/playbook-versioning/versions/${versionId}`)
      return response.data
    } catch (error) {
      console.error("Error getting version details:", error)
      throw error
    }
  },

  /**
   * Get all branches for a playbook
   */
  async getBranches(playbookId) {
    try {
      const response = await api.get(`/playbook-versioning/playbooks/${playbookId}/branches`)
      return response.data
    } catch (error) {
      console.error("Error getting branches:", error)
      throw error
    }
  },

  /**
   * Compare two specific versions
   */
  async compareVersions(version1Id, version2Id) {
    try {
      const response = await api.get(`/playbook-versioning/versions/compare/${version1Id}/${version2Id}`)
      return response.data
    } catch (error) {
      console.error("Error comparing versions:", error)
      throw error
    }
  },

  /**
   * Get versioning statistics
   */
  async getVersioningStatistics() {
    try {
      const response = await api.get("/playbook-versioning/statistics")
      return response.data
    } catch (error) {
      console.error("Error getting versioning statistics:", error)
      throw error
    }
  },
}

export default playbookVersioningService
