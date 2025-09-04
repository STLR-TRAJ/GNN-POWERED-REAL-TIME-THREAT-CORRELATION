<template>
  <span :class="badgeClasses">
    {{ severity }}
  </span>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'SeverityBadge',
  props: {
    severity: {
      type: String,
      required: true,
      validator: (value) => ['Critical', 'High', 'Medium', 'Low'].includes(value)
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    }
  },
  setup(props) {
    const severityStyles = {
      Critical: 'bg-red-100 text-red-800 border-red-200',
      High: 'bg-orange-100 text-orange-800 border-orange-200',
      Medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      Low: 'bg-green-100 text-green-800 border-green-200'
    }

    const sizeStyles = {
      sm: 'px-2 py-0.5 text-xs',
      md: 'px-2.5 py-0.5 text-sm',
      lg: 'px-3 py-1 text-base'
    }

    const badgeClasses = computed(() => {
      return [
        'inline-flex items-center font-medium rounded-full border',
        severityStyles[props.severity] || severityStyles.Medium,
        sizeStyles[props.size] || sizeStyles.md
      ].join(' ')
    })

    return {
      badgeClasses
    }
  }
}
</script>
