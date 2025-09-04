<template>
  <div class="relative h-64">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'SeverityChart',
  props: {
    data: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props)  {
    const chartCanvas = ref(null)
    let chartInstance = null

    const severityColors = {
      Critical: '#dc2626',
      High: '#ea580c',
      Medium: '#d97706',
      Low: '#65a30d'
    }

    const createChart = () => {
      if (!chartCanvas.value) return

      const ctx = chartCanvas.value.getContext('2d')
      
      const labels = Object.keys(props.data)
      const values = Object.values(props.data)
      const colors = labels.map(label => severityColors[label] || '#6b7280')

      if (chartInstance) {
        chartInstance.destroy()
      }

      chartInstance = new ChartJS(ctx, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: colors,
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                usePointStyle: true
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || ''
                  const value = context.parsed || 0
                  const total = context.dataset.data.reduce((a, b) => a + b, 0)
                  const percentage = total > 0 ? Math.round((value / total) * 100) : 0
                  return `${label}: ${value} (${percentage}%)`
                }
              }
            }
          }
        }
      })
    }

    onMounted(() => {
      createChart()
    })

    watch(() => props.data, () => {
      createChart()
    }, { deep: true })

    return {
      chartCanvas
    }
  }
}
</script>
