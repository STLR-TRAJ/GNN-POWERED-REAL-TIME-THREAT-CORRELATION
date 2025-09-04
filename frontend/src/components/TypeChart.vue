<template>
  <div class="relative h-64">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'TypeChart',
  props: {
    data: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null

    const typeColors = {
      ip: '#3b82f6',
      domain: '#8b5cf6',
      url: '#6366f1',
      file_hash: '#6b7280',
      cve: '#dc2626',
      email: '#10b981'
    }

    const createChart = () => {
      if (!chartCanvas.value) return

      const ctx = chartCanvas.value.getContext('2d')
      
      const labels = Object.keys(props.data).map(key => {
        const typeNames = {
          ip: 'IP Address',
          domain: 'Domain',
          url: 'URL',
          file_hash: 'File Hash',
          cve: 'CVE',
          email: 'Email'
        }
        return typeNames[key] || key.toUpperCase()
      })
      
      const values = Object.values(props.data)
      const colors = Object.keys(props.data).map(key => typeColors[key] || '#6b7280')

      if (chartInstance) {
        chartInstance.destroy()
      }

      chartInstance = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Threats',
            data: values,
            backgroundColor: colors,
            borderColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.parsed.y} threats`
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
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
