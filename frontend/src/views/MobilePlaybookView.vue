<template>
  <div class="mobile-playbook-view">
    <!-- Header -->
    <div class="mobile-header">
      <button @click="goBack" class="back-button">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h1 class="header-title">{{ playbook?.name || 'Playbook' }}</h1>
      <button @click="showMenu = !showMenu" class="menu-button">
        <i class="fas fa-ellipsis-v"></i>
      </button>
    </div>

    <!-- Menu Dropdown -->
    <div v-if="showMenu" class="menu-dropdown">
      <button @click="sharePlaybook" class="menu-item">
        <i class="fas fa-share"></i>
        Share
      </button>
      <button @click="downloadOffline" class="menu-item">
        <i class="fas fa-download"></i>
        Download for Offline
      </button>
      <button @click="showVersions = true" class="menu-item">
        <i class="fas fa-code-branch"></i>
        Versions
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading playbook...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <h3>Error Loading Playbook</h3>
      <p>{{ error }}</p>
      <button @click="loadPlaybook" class="retry-button">
        <i class="fas fa-redo"></i>
        Retry
      </button>
    </div>

    <!-- Playbook Content -->
    <div v-else-if="playbook" class="playbook-content">
      <!-- Playbook Info -->
      <div class="playbook-info">
        <div class="info-row">
          <span class="label">Category:</span>
          <span class="value">{{ playbook.category }}</span>
        </div>
        <div class="info-row">
          <span class="label">Difficulty:</span>
          <span class="value difficulty" :class="playbook.difficulty_level">
            {{ playbook.difficulty_level }}
          </span>
        </div>
        <div class="info-row">
          <span class="label">Duration:</span>
          <span class="value">{{ playbook.estimated_duration_minutes }} min</span>
        </div>
        <div class="info-row">
          <span class="label">Success Rate:</span>
          <span class="value">{{ Math.round(playbook.success_rate * 100) }}%</span>
        </div>
      </div>

      <!-- Description -->
      <div class="description-section">
        <h3>Description</h3>
        <p>{{ playbook.description }}</p>
      </div>

      <!-- Parameters -->
      <div v-if="playbook.parameters && Object.keys(playbook.parameters).length > 0" class="parameters-section">
        <h3>Parameters</h3>
        <div class="parameter-list">
          <div v-for="(param, key) in playbook.parameters" :key="key" class="parameter-item">
            <label :for="key" class="parameter-label">{{ param.label || key }}</label>
            <input
              :id="key"
              v-model="executionParameters[key]"
              :type="param.type || 'text'"
              :placeholder="param.description"
              :required="param.required"
              class="parameter-input"
            />
            <small v-if="param.description" class="parameter-description">
              {{ param.description }}
            </small>
          </div>
        </div>
      </div>

      <!-- Steps -->
      <div class="steps-section">
        <div class="steps-header">
          <h3>Steps ({{ playbook.steps.length }})</h3>
          <div class="progress-indicator">
            {{ currentStep + 1 }} / {{ playbook.steps.length }}
          </div>
        </div>

        <!-- Step Navigation -->
        <div class="step-navigation">
          <button
            @click="previousStep"
            :disabled="currentStep === 0"
            class="nav-button prev-button"
          >
            <i class="fas fa-chevron-left"></i>
            Previous
          </button>
          <button
            @click="nextStep"
            :disabled="currentStep === playbook.steps.length - 1"
            class="nav-button next-button"
          >
            Next
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>

        <!-- Current Step -->
        <div class="current-step">
          <div class="step-header">
            <h4>{{ playbook.steps[currentStep].name }}</h4>
            <span class="step-type">{{ playbook.steps[currentStep].type }}</span>
          </div>
          
          <div class="step-description">
            {{ playbook.steps[currentStep].description }}
          </div>

          <!-- Step Actions -->
          <div v-if="playbook.steps[currentStep].actions" class="step-actions">
            <h5>Actions:</h5>
            <ul>
              <li v-for="(action, index) in playbook.steps[currentStep].actions" :key="index">
                {{ action }}
              </li>
            </ul>
          </div>

          <!-- Step Results -->
          <div v-if="stepResults[currentStep]" class="step-results">
            <h5>Results:</h5>
            <div class="results-content">
              <pre>{{ JSON.stringify(stepResults[currentStep], null, 2) }}</pre>
            </div>
          </div>

          <!-- Step Controls -->
          <div class="step-controls">
            <button
              @click="executeStep(currentStep)"
              :disabled="executingStep === currentStep"
              class="execute-button"
            >
              <i v-if="executingStep === currentStep" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-play"></i>
              {{ executingStep === currentStep ? 'Executing...' : 'Execute Step' }}
            </button>
            
            <button
              v-if="stepResults[currentStep]"
              @click="markStepComplete(currentStep)"
              class="complete-button"
            >
              <i class="fas fa-check"></i>
              Mark Complete
            </button>
          </div>
        </div>

        <!-- Step Progress -->
        <div class="step-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${(completedSteps.length / playbook.steps.length) * 100}%` }"
            ></div>
          </div>
          <span class="progress-text">
            {{ completedSteps.length }} of {{ playbook.steps.length }} steps completed
          </span>
        </div>
      </div>

      <!-- Execution Controls -->
      <div class="execution-controls">
        <button
          @click="executePlaybook"
          :disabled="executing"
          class="execute-all-button"
        >
          <i v-if="executing" class="fas fa-spinner fa-spin"></i>
          <i v-else class="fas fa-play-circle"></i>
          {{ executing ? 'Executing...' : 'Execute All Steps' }}
        </button>
        
        <button
          v-if="executionResults"
          @click="shareResults"
          class="share-results-button"
        >
          <i class="fas fa-share-alt"></i>
          Share Results
        </button>
      </div>

      <!-- Execution Results -->
      <div v-if="executionResults" class="execution-results">
        <h3>Execution Results</h3>
        <div class="results-summary">
          <div class="result-item">
            <span class="label">Status:</span>
            <span class="value" :class="executionResults.status">
              {{ executionResults.status }}
            </span>
          </div>
          <div class="result-item">
            <span class="label">Duration:</span>
            <span class="value">{{ executionResults.duration_seconds }}s</span>
          </div>
          <div class="result-item">
            <span class="label">Steps Completed:</span>
            <span class="value">{{ executionResults.steps_completed || 0 }}</span>
          </div>
        </div>
        
        <div v-if="executionResults.findings" class="findings-section">
          <h4>Findings</h4>
          <div class="findings-list">
            <div
              v-for="(finding, index) in executionResults.findings"
              :key="index"
              class="finding-item"
              :class="finding.severity"
            >
              <div class="finding-header">
                <span class="finding-title">{{ finding.title }}</span>
                <span class="finding-severity">{{ finding.severity }}</span>
              </div>
              <p class="finding-description">{{ finding.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Versions Modal -->
    <div v-if="showVersions" class="modal-overlay" @click="showVersions = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Playbook Versions</h3>
          <button @click="showVersions = false" class="close-button">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="loadingVersions" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading versions...</p>
          </div>
          <div v-else class="versions-list">
            <div
              v-for="version in versions"
              :key="version.id"
              class="version-item"
              :class="{ active: version.is_active }"
              @click="switchVersion(version)"
            >
              <div class="version-info">
                <span class="version-number">v{{ version.version_number }}</span>
                <span v-if="version.is_active" class="active-badge">Active</span>
              </div>
              <p class="version-message">{{ version.commit_message }}</p>
              <div class="version-meta">
                <span class="version-author">{{ version.author }}</span>
                <span class="version-date">{{ formatDate(version.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Offline Indicator -->
    <div v-if="isOffline" class="offline-indicator">
      <i class="fas fa-wifi-slash"></i>
      Offline Mode
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { huntPlaybooksService } from '@/services/huntPlaybooks'
import { playbookVersioningService } from '@/services/playbookVersioning'

export default {
  name: 'MobilePlaybookView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Reactive data
    const playbook = ref(null)
    const versions = ref([])
    const loading = ref(true)
    const loadingVersions = ref(false)
    const error = ref(null)
    const showMenu = ref(false)
    const showVersions = ref(false)
    const currentStep = ref(0)
    const executingStep = ref(null)
    const executing = ref(false)
    const executionResults = ref(null)
    const stepResults = reactive({})
    const completedSteps = ref([])
    const executionParameters = reactive({})
    const isOffline = ref(!navigator.onLine)
    
    // Computed properties
    const playbookId = computed(() => parseInt(route.params.id))
    
    // Methods
    const loadPlaybook = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await huntPlaybooksService.getPlaybook(playbookId.value)
        playbook.value = response.data.playbook
        
        // Initialize execution parameters
        if (playbook.value.parameters) {
          Object.keys(playbook.value.parameters).forEach(key => {
            executionParameters[key] = playbook.value.parameters[key].default || ''
          })
        }
        
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to load playbook'
        console.error('Error loading playbook:', err)
      } finally {
        loading.value = false
      }
    }
    
    const loadVersions = async () => {
      try {
        loadingVersions.value = true
        const response = await playbookVersioningService.getVersionHistory(playbookId.value)
        versions.value = response.data.versions
      } catch (err) {
        console.error('Error loading versions:', err)
      } finally {
        loadingVersions.value = false
      }
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    const nextStep = () => {
      if (currentStep.value < playbook.value.steps.length - 1) {
        currentStep.value++
      }
    }
    
    const previousStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }
    
    const executeStep = async (stepIndex) => {
      try {
        executingStep.value = stepIndex
        
        const response = await huntPlaybooksService.executeStep(
          playbookId.value,
          stepIndex,
          executionParameters
        )
        
        stepResults[stepIndex] = response.data.results
        
      } catch (err) {
        console.error('Error executing step:', err)
        stepResults[stepIndex] = {
          error: err.response?.data?.message || 'Step execution failed'
        }
      } finally {
        executingStep.value = null
      }
    }
    
    const markStepComplete = (stepIndex) => {
      if (!completedSteps.value.includes(stepIndex)) {
        completedSteps.value.push(stepIndex)
      }
    }
    
    const executePlaybook = async () => {
      try {
        executing.value = true
        
        const response = await huntPlaybooksService.executePlaybook(
          playbookId.value,
          executionParameters
        )
        
        executionResults.value = response.data.results
        
        // Mark all steps as completed if execution was successful
        if (response.data.results.status === 'completed') {
          completedSteps.value = Array.from({ length: playbook.value.steps.length }, (_, i) => i)
        }
        
      } catch (err) {
        console.error('Error executing playbook:', err)
        executionResults.value = {
          status: 'failed',
          error: err.response?.data?.message || 'Playbook execution failed'
        }
      } finally {
        executing.value = false
      }
    }
    
    const sharePlaybook = async () => {
      try {
        if (navigator.share) {
          await navigator.share({
            title: playbook.value.name,
            text: playbook.value.description,
            url: window.location.href
          })
        } else {
          // Fallback: copy to clipboard
          await navigator.clipboard.writeText(window.location.href)
          alert('Playbook URL copied to clipboard!')
        }
      } catch (err) {
        console.error('Error sharing playbook:', err)
      }
      showMenu.value = false
    }
    
    const shareResults = async () => {
      try {
        const resultsText = `Playbook: ${playbook.value.name}\nStatus: ${executionResults.value.status}\nDuration: ${executionResults.value.duration_seconds}s`
        
        if (navigator.share) {
          await navigator.share({
            title: `${playbook.value.name} - Results`,
            text: resultsText
          })
        } else {
          await navigator.clipboard.writeText(resultsText)
          alert('Results copied to clipboard!')
        }
      } catch (err) {
        console.error('Error sharing results:', err)
      }
    }
    
    const downloadOffline = async () => {
      try {
        // Store playbook data in localStorage for offline access
        const offlineData = {
          playbook: playbook.value,
          timestamp: Date.now()
        }
        
        localStorage.setItem(`offline_playbook_${playbookId.value}`, JSON.stringify(offlineData))
        alert('Playbook downloaded for offline use!')
        
      } catch (err) {
        console.error('Error downloading for offline:', err)
        alert('Failed to download playbook for offline use')
      }
      showMenu.value = false
    }
    
    const switchVersion = async (version) => {
      try {
        await playbookVersioningService.activateVersion(version.id)
        await loadPlaybook()
        showVersions.value = false
        alert(`Switched to version ${version.version_number}`)
      } catch (err) {
        console.error('Error switching version:', err)
        alert('Failed to switch version')
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    // Handle online/offline status
    const handleOnline = () => {
      isOffline.value = false
    }
    
    const handleOffline = () => {
      isOffline.value = true
    }
    
    // Lifecycle hooks
    onMounted(async () => {
      await loadPlaybook()
      
      // Add event listeners for online/offline status
      window.addEventListener('online', handleOnline)
      window.addEventListener('offline', handleOffline)
      
      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.menu-button') && !e.target.closest('.menu-dropdown')) {
          showMenu.value = false
        }
      })
    })
    
    return {
      // Data
      playbook,
      versions,
      loading,
      loadingVersions,
      error,
      showMenu,
      showVersions,
      currentStep,
      executingStep,
      executing,
      executionResults,
      stepResults,
      completedSteps,
      executionParameters,
      isOffline,
      
      // Methods
      loadPlaybook,
      loadVersions,
      goBack,
      nextStep,
      previousStep,
      executeStep,
      markStepComplete,
      executePlaybook,
      sharePlaybook,
      shareResults,
      downloadOffline,
      switchVersion,
      formatDate
    }
  }
}
</script>

<style scoped>
.mobile-playbook-view {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-bottom: 80px;
}

.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: white;
  border-bottom: 1px solid #e9ecef;
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-button, .menu-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #6c757d;
  padding: 0.5rem;
  cursor: pointer;
}

.header-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  flex: 1;
  text-align: center;
  padding: 0 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  right: 1rem;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 200;
  min-width: 200px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.menu-item:hover {
  background-color: #f8f9fa;
}

.menu-item i {
  width: 1rem;
  color: #6c757d;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e9ecef;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container i {
  font-size: 3rem;
  color: #dc3545;
  margin-bottom: 1rem;
}

.retry-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-top: 1rem;
}

.playbook-content {
  padding: 1rem;
}

.playbook-info {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #6c757d;
}

.value {
  font-weight: 500;
}

.difficulty.beginner {
  color: #28a745;
}

.difficulty.intermediate {
  color: #ffc107;
}

.difficulty.advanced {
  color: #dc3545;
}

.description-section, .parameters-section, .steps-section {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.description-section h3, .parameters-section h3, .steps-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.parameter-item {
  margin-bottom: 1rem;
}

.parameter-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #495057;
}

.parameter-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.parameter-description {
  display: block;
  margin-top: 0.25rem;
  color: #6c757d;
  font-size: 0.875rem;
}

.steps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.progress-indicator {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.step-navigation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.nav-button {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-button:not(:disabled):hover {
  background-color: #f8f9fa;
}

.current-step {
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.step-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.step-type {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.step-description {
  color: #6c757d;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.step-actions h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  font-weight: 600;
}

.step-actions ul {
  margin: 0;
  padding-left: 1.5rem;
}

.step-actions li {
  margin-bottom: 0.25rem;
  color: #6c757d;
}

.step-results {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.step-results h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  font-weight: 600;
}

.results-content pre {
  margin: 0;
  font-size: 0.8rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.step-controls {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.execute-button, .complete-button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.execute-button {
  background-color: #007bff;
  color: white;
}

.execute-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.complete-button {
  background-color: #28a745;
  color: white;
}

.step-progress {
  margin-top: 1rem;
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: #e9ecef;
  border-radius: 0.25rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background-color: #28a745;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  color: #6c757d;
}

.execution-controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.execute-all-button, .share-results-button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.execute-all-button {
  background-color: #007bff;
  color: white;
}

.execute-all-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.share-results-button {
  background-color: #17a2b8;
  color: white;
}

.execution-results {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.execution-results h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.results-summary {
  margin-bottom: 1rem;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.result-item:last-child {
  border-bottom: none;
}

.value.completed {
  color: #28a745;
  font-weight: 600;
}

.value.failed {
  color: #dc3545;
  font-weight: 600;
}

.findings-section h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.finding-item {
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 0.75rem;
  border-left: 4px solid;
}

.finding-item.Low {
  background-color: #d1ecf1;
  border-left-color: #17a2b8;
}

.finding-item.Medium {
  background-color: #fff3cd;
  border-left-color: #ffc107;
}

.finding-item.High {
  background-color: #f8d7da;
  border-left-color: #dc3545;
}

.finding-item.Critical {
  background-color: #f5c6cb;
  border-left-color: #721c24;
}

.finding-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.finding-title {
  font-weight: 600;
}

.finding-severity {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  background-color: rgba(0, 0, 0, 0.1);
}

.finding-description {
  margin: 0;
  color: #6c757d;
  line-height: 1.4;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.version-item {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.version-item:hover {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.version-item.active {
  border-color: #28a745;
  background-color: #d4edda;
}

.version-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.version-number {
  font-weight: 600;
  font-size: 1rem;
}

.active-badge {
  background-color: #28a745;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.version-message {
  margin: 0 0 0.5rem 0;
  color: #495057;
  font-size: 0.9rem;
}

.version-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #6c757d;
}

.offline-indicator {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  background-color: #ffc107;
  color: #212529;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  z-index: 1000;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .mobile-header {
    padding: 0.75rem;
  }
  
  .header-title {
    font-size: 1rem;
  }
  
  .playbook-content {
    padding: 0.75rem;
  }
  
  .step-controls {
    flex-direction: column;
  }
  
  .execution-controls {
    flex-direction: column;
  }
}
</style>
