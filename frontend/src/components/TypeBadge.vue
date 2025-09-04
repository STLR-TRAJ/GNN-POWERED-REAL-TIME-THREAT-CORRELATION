<template>
  <span :class="badgeClasses">
    <component :is="iconComponent" class="w-3 h-3 mr-1" />
    {{ displayName }}
  </span>
</template>

<script>
import { computed } from 'vue'
import { Globe, Hash, Link, FileText, Shield } from 'lucide-vue-next'

export default {
  name: 'TypeBadge',
  components: {
    Globe, Hash, Link, FileText, Shield
  },
  props: {
    type: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const typeConfig = {
      ip: {
        name: 'IP',
        icon: Globe,
        classes: 'bg-blue-100 text-blue-800 border-blue-200'
      },
      domain: {
        name: 'Domain',
        icon: Globe,
        classes: 'bg-purple-100 text-purple-800 border-purple-200'
      },
      url: {
        name: 'URL',
        icon: Link,
        classes: 'bg-indigo-100 text-indigo-800 border-indigo-200'
      },
      file_hash: {
        name: 'Hash',
        icon: Hash,
        classes: 'bg-gray-100 text-gray-800 border-gray-200'
      },
      cve: {
        name: 'CVE',
        icon: Shield,
        classes: 'bg-red-100 text-red-800 border-red-200'
      },
      email: {
        name: 'Email',
        icon: FileText,
        classes: 'bg-green-100 text-green-800 border-green-200'
      }
    }

    const config = computed(() => {
      return typeConfig[props.type] || {
        name: props.type.toUpperCase(),
        icon: FileText,
        classes: 'bg-gray-100 text-gray-800 border-gray-200'
      }
    })

    const displayName = computed(() => config.value.name)
    const iconComponent = computed(() => config.value.icon)
    
    const badgeClasses = computed(() => {
      return [
        'inline-flex items-center px-2 py-0.5 text-xs font-medium rounded border',
        config.value.classes
      ].join(' ')
    })

    return {
      displayName,
      iconComponent,
      badgeClasses
    }
  }
}
</script>
