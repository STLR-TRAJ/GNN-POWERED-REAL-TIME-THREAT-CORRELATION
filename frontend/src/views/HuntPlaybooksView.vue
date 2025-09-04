<template>
  <div class="hunt-playbooks-view">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Hunt Playbooks</h1>
          <p class="text-sm text-gray-600 mt-1">Predefined threat hunting scenarios and workflows</p>
        </div>
        <div class="flex space-x-3">
          <button
            @click="showCreateModal = true"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <i class="fas fa-plus mr-2"></i>
            Create Playbook
          </button>
          <button
            @click="showImportModal = true"
            class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            <i class="fas fa-upload mr-2"></i>
            Import
          </button>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
      <div class="flex items-center space-x-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search playbooks..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="selectedCategory"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category.value" :value="category.value">
            {{ category.name }}
          </option>
        </select>
        <select
          v-model="selectedSeverity"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Severities</option>
          <option v-for="severity in severities" :key="severity.value" :value="severity.value">
            {{ severity.name }}
          </option>
        </select>
        <button
          @click="loadPlaybooks"
          class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
        >
          <i class="fas fa-search mr-2"></i>
          Filter
        </button>
      </div>
    </div>

    <!-- Playbooks Grid -->
    <div class="p-6">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-600 mt-4">Loading playbooks...</p>
      </div>

      <div v-else-if="filteredPlaybooks.length === 0" class="text-center py-12">
        <div class="mx-auto h-12 w-12 text-gray-400">
          <i class="fas fa-book text-4xl"></i>
        </div>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No playbooks found</h3>
        <p class="mt-1 text-sm text-gray-500">Try adjusting your search criteria or create a new playbook</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="playbook in filteredPlaybooks"
          :key="playbook.playbook_id"
          class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
          @click="viewPlaybook(playbook)"
        >
          <div class="p-6">
            <!-- Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ playbook.name }}</h3>
                <p class="text-sm text-gray-600 line-clamp-2">{{ playbook.description }}</p>
              </div>
              <div class="ml-4">
                <span
                  :class="getSeverityClass(playbook.severity)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ playbook.severity.toUpperCase() }}
                </span>
              </div>
            </div>

            <!-- Metadata -->
            <div class="space-y-2 mb-4">
              <div class="flex items-center text-sm text-gray-600">
                <i class="fas fa-folder mr-2"></i>
                <span>{{ formatCategory(playbook.category) }}</span>
              </div>
              <div class="flex items-center text-sm text-gray-600">
                <i class="fas fa-clock mr-2"></i>
                <span>~{{ playbook.estimated_duration }} minutes</span>
              </div>
              <div class="flex items-center text-sm text-gray-600">
                <i class="fas fa-list mr-2"></i>
                <span>{{ playbook.step_count }} steps</span>
              </div>
            </div>

            <!-- Tags -->
            <div class="mb-4">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="tag in playbook.tags.slice(0, 3)"
                  :key="tag"
                  class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ tag }}
                </span>
                <span
                  v-if="playbook.tags.length > 3"
                  class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600"
                >
                  +{{ playbook.tags.length - 3 }} more
                </span>
              </div>
            </div>

            <!-- MITRE ATT&CK -->
            <div v-if="playbook.mitre_techniques.length > 0" class="mb-4">
              <div class="text-xs text-gray-500 mb-1">MITRE ATT&CK</div>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="technique in playbook.mitre_techniques.slice(0, 2)"
                  :key="technique"
                  class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-red-100 text-red-800"
                >
                  {{ technique }}
                </span>
                <span
                  v-if="playbook.mitre_techniques.length > 2"
                  class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600"
                >
                  +{{ playbook.mitre_techniques.length - 2 }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-200">
              <div class="text-xs text-gray-500">
                Updated {{ formatDate(playbook.last_updated) }}
              </div>
              <div class="flex space-x-2">
                <button
                  @click.stop="executePlaybook(playbook)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Execute
                </button>
                <button
                  @click.stop="showPlaybookMenu(playbook, $event)"
                  class="text-gray-400 hover:text-gray-600"
                >
                  <i class="fas fa-ellipsis-v"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Playbook Detail Modal -->
    <div v-if="selectedPlaybook && showDetailModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 shadow-lg rounded-md bg-white max-h-[80vh] overflow-y-auto">
        <PlaybookDetailModal
          :playbook="selectedPlaybook"
          @close="showDetailModal = false"
          @execute="executePlaybook"
          @edit="editPlaybook"
          @export="exportPlaybook"
          @delete="deletePlaybook"
        />
      </div>
    </div>

    <!-- Create/Edit Playbook Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 shadow-lg rounded-md bg-white max-h-[90vh] overflow-y-auto">
        <PlaybookEditorModal
          :playbook="editingPlaybook"
          :categories="categories"
          :severities="severities"
          :templates="playbookTemplates"
          @close="closeCreateEditModal"
          @save="savePlaybook"
        />
      </div>
    </div>

    <!-- Import Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <PlaybookImportModal
          @close="showImportModal = false"
          @import="importPlaybook"
        />
      </div>
    </div>

    <!-- Execution Modal -->
    <div v-if="showExecutionModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-2/3 shadow-lg rounded-md bg-white max-h-[80vh] overflow-y-auto">
        <PlaybookExecutionModal
          :playbook="executingPlaybook"
          :execution-result="executionResult"
          @close="showExecutionModal = false"
          @execute="startPlaybookExecution"
        />
      </div>
    </div>

    <!-- Context Menu -->
    <div
      v-if="showContextMenu"
      :style="{ top: contextMenuY + 'px', left: contextMenuX + 'px' }"
      class="fixed bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50"
    >
      <button
        @click="viewPlaybook(contextMenuPlaybook)"
        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
      >
        <i class="fas fa-eye mr-2"></i>View Details
      </button>
      <button
        @click="executePlaybook(contextMenuPlaybook)"
        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
      >
        <i class="fas fa-play mr-2"></i>Execute
      </button>
      <button
        @click="editPlaybook(contextMenuPlaybook)"
        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
      >
        <i class="fas fa-edit mr-2"></i>Edit
      </button>
      <button
        @click="exportPlaybook(contextMenuPlaybook)"
        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
      >
        <i class="fas fa-download mr-2"></i>Export
      </button>
      <hr class="my-1">
      <button
        @click="deletePlaybook(contextMenuPlaybook)"
        class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
      >
        <i class="fas fa-trash mr-2"></i>Delete
      </button>
    </div>

    <!-- Loading Overlay -->
    <div v-if="operationLoading" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 shadow-lg">
        <div class="flex items-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
          <span class="text-gray-700">{{ operationMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import PlaybookDetailModal from '@/components/PlaybookDetailModal.vue'
import PlaybookEditorModal from '@/components/PlaybookEditorModal.vue'
import PlaybookImportModal from '@/components/PlaybookImportModal.vue'
import PlaybookExecutionModal from '@/components/PlaybookExecutionModal.vue'
import { huntPlaybooksService } from '@/services/huntPlaybooks'

export default {
  name: 'HuntPlaybooksView',
  components: {
    PlaybookDetailModal,
    PlaybookEditorModal,
    PlaybookImportModal,
    PlaybookExecutionModal
  },
  setup() {
    const playbooks = ref([])
    const categories = ref([])
    const severities = ref([])
    const playbookTemplates = ref([])
    const loading = ref(false)
    const operationLoading = ref(false)
    const operationMessage = ref('')

    // Search and filters
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const selectedSeverity = ref('')

    // Modals
    const showDetailModal = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showImportModal = ref(false)
    const showExecutionModal = ref(false)

    // Selected items
    const selectedPlaybook = ref(null)
    const editingPlaybook = ref(null)
    const executingPlaybook = ref(null)
    const executionResult = ref(null)

    // Context menu
    const showContextMenu = ref(false)
    const contextMenuX = ref(0)
    const contextMenuY = ref(0)
    const contextMenuPlaybook = ref(null)

    const filteredPlaybooks = computed(() => {
      let filtered = playbooks.value

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.name.toLowerCase().includes(query) ||
          p.description.toLowerCase().includes(query) ||
          p.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }

      if (selectedCategory.value) {
        filtered = filtered.filter(p => p.category === selectedCategory.value)
      }

      if (selectedSeverity.value) {
        filtered = filtered.filter(p => p.severity === selectedSeverity.value)
      }

      return filtered
    })

    const loadPlaybooks = async () => {
      loading.value = true
      try {
        const response = await huntPlaybooksService.listPlaybooks({
          category: selectedCategory.value || undefined,
          severity: selectedSeverity.value || undefined
        })
        playbooks.value = response.playbooks
      } catch (error) {
        console.error('Failed to load playbooks:', error)
      } finally {
        loading.value = false
      }
    }

    const loadMetadata = async () => {
      try {
        const [categoriesRes, severitiesRes, templatesRes] = await Promise.all([
          huntPlaybooksService.getCategories(),
          huntPlaybooksService.getSeverities(),
          huntPlaybooksService.getTemplates()
        ])
        
        categories.value = categoriesRes.categories
        severities.value = severitiesRes.severities
        playbookTemplates.value = templatesRes.templates
      } catch (error) {
        console.error('Failed to load metadata:', error)
      }
    }

    const viewPlaybook = async (playbook) => {
      try {
        const response = await huntPlaybooksService.getPlaybook(playbook.playbook_id)
        selectedPlaybook.value = response.playbook
        showDetailModal.value = true
        hideContextMenu()
      } catch (error) {
        console.error('Failed to load playbook details:', error)
      }
    }

    const executePlaybook = (playbook) => {
      executingPlaybook.value = playbook
      executionResult.value = null
      showExecutionModal.value = true
      hideContextMenu()
    }

    const startPlaybookExecution = async (playbookId, parameters) => {
      operationLoading.value = true
      operationMessage.value = 'Executing playbook...'
      
      try {
        const response = await huntPlaybooksService.executePlaybook(playbookId, parameters)
        executionResult.value = response.execution
      } catch (error) {
        console.error('Playbook execution failed:', error)
      } finally {
        operationLoading.value = false
      }
    }

    const editPlaybook = (playbook) => {
      editingPlaybook.value = playbook
      showEditModal.value = true
      hideContextMenu()
    }

    const savePlaybook = async (playbookData) => {
      operationLoading.value = true
      operationMessage.value = editingPlaybook.value ? 'Updating playbook...' : 'Creating playbook...'
      
      try {
        if (editingPlaybook.value) {
          await huntPlaybooksService.updatePlaybook(editingPlaybook.value.playbook_id, playbookData)
        } else {
          await huntPlaybooksService.createPlaybook(playbookData)
        }
        
        closeCreateEditModal()
        await loadPlaybooks()
      } catch (error) {
        console.error('Failed to save playbook:', error)
      } finally {
        operationLoading.value = false
      }
    }

    const exportPlaybook = async (playbook) => {
      try {
        const response = await huntPlaybooksService.exportPlaybook(playbook.playbook_id)
        
        const blob = new Blob([JSON.stringify(response.playbook_data, null, 2)], { 
          type: 'application/json' 
        })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${playbook.name.replace(/\s+/g, '_')}_playbook.json`
        a.click()
        window.URL.revokeObjectURL(url)
        
        hideContextMenu()
      } catch (error) {
        console.error('Failed to export playbook:', error)
      }
    }

    const importPlaybook = async (playbookData) => {
      operationLoading.value = true
      operationMessage.value = 'Importing playbook...'
      
      try {
        await huntPlaybooksService.importPlaybook(playbookData)
        showImportModal.value = false
        await loadPlaybooks()
      } catch (error) {
        console.error('Failed to import playbook:', error)
      } finally {
        operationLoading.value = false
      }
    }

    const deletePlaybook = async (playbook) => {
      if (!confirm(`Are you sure you want to delete "${playbook.name}"?`)) {
        return
      }

      operationLoading.value = true
      operationMessage.value = 'Deleting playbook...'
      
      try {
        await huntPlaybooksService.deletePlaybook(playbook.playbook_id)
        await loadPlaybooks()
        hideContextMenu()
      } catch (error) {
        console.error('Failed to delete playbook:', error)
      } finally {
        operationLoading.value = false
      }
    }

    const showPlaybookMenu = (playbook, event) => {
      event.preventDefault()
      contextMenuPlaybook.value = playbook
      contextMenuX.value = event.clientX
      contextMenuY.value = event.clientY
      showContextMenu.value = true
    }

    const hideContextMenu = () => {
      showContextMenu.value = false
      contextMenuPlaybook.value = null
    }

    const closeCreateEditModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingPlaybook.value = null
    }

    const getSeverityClass = (severity) => {
      const classes = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-orange-100 text-orange-800',
        critical: 'bg-red-100 text-red-800'
      }
      return classes[severity.toLowerCase()] || 'bg-gray-100 text-gray-800'
    }

    const formatCategory = (category) => {
      return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const handleClickOutside = (event) => {
      if (showContextMenu.value) {
        hideContextMenu()
      }
    }

    onMounted(async () => {
      await Promise.all([loadPlaybooks(), loadMetadata()])
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      playbooks,
      categories,
      severities,
      playbookTemplates,
      loading,
      operationLoading,
      operationMessage,
      searchQuery,
      selectedCategory,
      selectedSeverity,
      filteredPlaybooks,
      showDetailModal,
      showCreateModal,
      showEditModal,
      showImportModal,
      showExecutionModal,
      selectedPlaybook,
      editingPlaybook,
      executingPlaybook,
      executionResult,
      showContextMenu,
      contextMenuX,
      contextMenuY,
      contextMenuPlaybook,
      loadPlaybooks,
      viewPlaybook,
      executePlaybook,
      startPlaybookExecution,
      editPlaybook,
      savePlaybook,
      exportPlaybook,
      importPlaybook,
      deletePlaybook,
      showPlaybookMenu,
      hideContextMenu,
      closeCreateEditModal,
      getSeverityClass,
      formatCategory,
      formatDate
    }
  }
}
</script>

<style scoped>
.hunt-playbooks-view {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
