<template>
  <div
    class="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
    :class="{ 'border-l-4': !compact }"
    :style="compact ? {} : { borderLeftColor: severityColors[threat.severity] }"
    @click="$emit('click', threat)"
  >
    <div class="flex items-start justify-between">
      <div class="flex-1 min-w-0">
        <div class="flex items-center space-x-2 mb-2">
          <SeverityBadge :severity="threat.severity" :size="compact ? 'sm' : 'md'" />
          <TypeBadge :type="threat.type" />
          <span v-if="!compact" class="text-xs text-gray-500">{{ threat.source }}</span>
        </div>
        
        <div class="mb-2">
          <p class="text-sm font-medium text-gray-900 font-mono break-all">
            {{ threat.value }}
          </p>
          <p v-if="threat.description && !compact" class="text-sm text-gray-600 mt-1 line-clamp-2">
            {{ threat.description }}
          </p>
        </div>
        
        <div class="flex items-center space-x-4 text-xs text-gray-500">
          <div class="flex items-center space-x-1">
            <span>Confidence:</span>
            <span class="font-medium">{{ threat.confidence }}%</span>
          </div>
          <div class="flex items-center space-x-1">
            <Clock class="w-3 h-3" />
            <span>{{ formatTimeAgo(threat.last_seen) }}</span>
          </div>
        </div>
        
        <div v-if="threat.tags && threat.tags.length > 0 && !compact" class="mt-2">
          <div class="flex flex-wrap gap-1">
            <span
              v-for="tag in threat.tags.slice(0, 3)"
              :key="tag"
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
            >
              {{ tag }}
            </span>
            <span
              v-if="threat.tags.length > 3"
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
            >
              +{{ threat.tags.length - 3 }} more
            </span>
          </div>
        </div>
      </div>
      
      <div v-if="!compact" class="ml-4 flex-shrink-0">
        <button
          @click.stop="$emit('analyze', threat)"
          class="inline-flex items-center px-2 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          <Search class="w-3 h-3 mr-1" />
          Analyze
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDistanceToNow } from 'date-fns'
import { Clock, Search } from 'lucide-vue-next'
import SeverityBadge from './SeverityBadge.vue'
import TypeBadge from './TypeBadge.vue'

export default {
  name: 'ThreatCard',
  components: {
    SeverityBadge,
    TypeBadge,
    Clock,
    Search
  },
  props: {
    threat: {
      type: Object,
      required: true
    },
    compact: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click', 'analyze'],
  setup() {
    const severityColors = {
      Critical: '#dc2626',
      High: '#ea580c',
      Medium: '#d97706',
      Low: '#65a30d'
    }

    const formatTimeAgo = (dateString) => {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true })
    }

    return {
      severityColors,
      formatTimeAgo
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
