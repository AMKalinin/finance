<script setup lang="ts">
  import { computed } from 'vue'
  import { Pie } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'


  ChartJS.register(ArcElement, Tooltip, Legend)

  const props = defineProps<{
    accounts: Account[]
  }>()


  const processedData = computed(() => {
    if (!props.accounts || props.accounts.length === 0) {
      return []
    }
    const sortedAccounts = [...props.accounts].sort((a, b) => (b.balance || 0) - (a.balance || 0))
    const top5 = sortedAccounts.slice(0, 5)
    const others = sortedAccounts.slice(5)

    const othersTotal = others.reduce((sum: number, acc: any) => sum + (acc.balance || 0), 0)

    if (others.length > 0) {
      top5.push({
        name: 'Others',
        balance: othersTotal
      })
    }
    return top5
  })

  const chartLabels = computed(() => {
    if (!processedData.value || processedData.value.length === 0) return ['No accounts']
    return processedData.value.map(acc => acc.name)
  })

  const chartData = computed(() => ({
    labels: chartLabels.value,
    datasets: [{
      data: processedData.value.map(acc => acc.balance || 0),
      backgroundColor: [
        'rgba(147, 51, 234, 0.8)',  // Purple
        'rgba(234, 179, 8, 0.8)',   // Yellow
        'rgba(34, 197, 94, 0.8)',   // Green
        'rgba(59, 130, 246, 0.8)',  // Blue
        'rgba(236, 72, 153, 0.8)',  // Pink
        'rgba(107, 114, 128, 0.8)', // Gray (for Others)
      ],
      borderColor: [
        'rgb(147, 51, 234)',
        'rgb(234, 179, 8)',
        'rgb(34, 197, 94)',
        'rgb(59, 130, 246)',
        'rgb(236, 72, 153)',
        'rgb(107, 114, 128)',
      ],
      borderWidth: 1,
      hoverOffset: 4
    }]
  }))

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: window.innerWidth < 640 ? 1 : 2, // Квадрат на мобильных, прямоугольник на десктопе
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          usePointStyle: true,
          pointStyle: 'circle',
          padding: 15,
          font: {
            size: window.innerWidth < 640 ? 10 : 12
          },
          generateLabels: (chart: any) => {
            const labels = chart.legend?.labels || []
            return labels.map((label: any) => ({
              text: `${label.text} (${Math.round(label.dataset.data[0] / 
                chart.data.datasets[0].data.reduce((a, b) => a + b, 0) * 100)}%)`,
              fillStyle: label.fillStyle,
              hidden: label.hidden,
              index: label.index,
              textBaseline: 'middle'
            }))
          }
        }
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const value = context.raw;
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${value.toLocaleString('ru-RU')} RUB (${percentage}%)`;
          }
        }
      }
    },
    layout: {
      padding: window.innerWidth < 640 ? 5 : 10
    }
  }

  const total = computed(() => props.accounts.reduce((sum, acc) => sum + (acc.balance || 0), 0))
</script>

<template>
  <div class="relative">
    <!-- Chart container with responsive height -->
    <div :class="[
      'w-full h-48 md:h-56 lg:h-64 flex items-center justify-center',
      processedData.value.length === 0 ? '' : ''
    ]">
      <Pie 
        v-if="processedData.value.length > 0"
        :data="chartData" 
        :options="chartOptions" 
      />
      
      <!-- Empty state -->
      <div v-else class="text-center text-gray-500 dark:text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
        </svg>
        <p class="text-sm">No account data</p>
      </div>
    </div>

    <!-- Total balance overlay -->
    <div v-if="processedData.value.length > 0" class="absolute top-4 right-4 md:top-6 md:right-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg px-3 py-2 shadow-sm">
      <p class="text-xs text-gray-500 dark:text-gray-400">Total Balance</p>
      <p class="text-lg md:text-xl font-bold text-gray-900 dark:text-white">{{ total.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} RUB</p>
    </div>

    <!-- Legend for mobile - show below chart -->
    <div v-if="processedData.value.length > 0 && window.innerWidth < 640" class="mt-3 px-2">
      <div class="grid grid-cols-3 gap-2 text-xs">
        <div v-for="(acc, idx) in processedData.value.slice(0, 6)" :key="idx" 
             class="flex items-center gap-1 truncate"
             :title="acc.name">
          <span class="w-2 h-2 rounded-full flex-shrink-0" 
                :style="{ backgroundColor: chartOptions.plugins!.legend!['labels']?.generateLabels({data: chartData})[idx]?.fillStyle || chartData.datasets[0].borderColor[idx] }"></span>
          <span class="truncate text-gray-600 dark:text-gray-400">{{ acc.name.substring(0, 8) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Mobile optimizations */
@media (max-width: 639px) {
  .h-48 {
    height: 200px; /* Фиксированная высота для мобильных */
  }
}
</style>
