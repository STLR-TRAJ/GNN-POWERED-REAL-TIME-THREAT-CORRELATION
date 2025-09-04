<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <component
            :is="iconComponent"
            :class="[
              'h-8 w-8',
              colorClasses[color] || 'text-gray-600'
            ]"
          />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
            <dd class="flex items-baseline">
              <div class="text-2xl font-semibold text-gray-900">
                {{ formattedValue }}
              </div>
              <div v-if="trend" class="ml-2 flex items-baseline text-sm">
                <component
                  :is="trend.direction === 'up' ? TrendingUp : TrendingDown"
                  :class="[
                    'self-center flex-shrink-0 h-4 w-4',
                    trend.isPositive ? 'text-green-500' : 'text-red-500'
                  ]"
                />
                <span :class="[
                  'ml-1',
                  trend.isPositive ? 'text-green-600' : 'text-red-600'
                ]">
                  {{ trend.value }}%
                </span>
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import {
  Shield, AlertTriangle, AlertOctagon, TrendingUp, TrendingDown,
  Activity, Clock, Users, Database
} from 'lucide-vue-next'

export default {
  name: 'SummaryCard',
  components: {
    Shield, AlertTriangle, AlertOctagon, TrendingUp, TrendingDown,
    Activity, Clock, Users, Database
  },
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [Number, String],
      required: true
    },
    icon: {
      type: String,
      default: 'Shield'
    },
    color: {
      type: String,
      default: 'blue'
    },
    trend: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const colorClasses = {
      blue: 'text-blue-600',
      green: 'text-green-600',
      orange: 'text-orange-600',
      red: 'text-red-600',
      purple: 'text-purple-600',
      gray: 'text-gray-600'
    }

    const iconComponents = {
      Shield,
      AlertTriangle,
      AlertOctagon,
      TrendingUp,
      Activity,
      Clock,
      Users,
      Database
    }

    const iconComponent = computed(() => {
      return iconComponents[props.icon] || Shield
    })

    const formattedValue = computed(() => {
      if (typeof props.value === 'number') {
        return props.value.toLocaleString()
      }
      return props.value
    })

    return {
      colorClasses,
      iconComponent,
      formattedValue,
      TrendingUp,
      TrendingDown
    }
  }
}
</script>
