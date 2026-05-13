<script setup lang="ts">
  import { computed } from 'vue'
  import { Pie } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'


  ChartJS.register(ArcElement, Tooltip, Legend)

  const props = defineProps<{
    transactions: any[],
    categories: any[]
  }>()

  // Фильтруем только Debit транзакции для анализа расходов
  const debitTransactions = computed(() => {
    if (!props.transactions) return []
    return props.transactions.filter((tx: any) => tx.type === 'Debit')
  })

  const processedData = computed(() => {
    if (debitTransactions.value.length === 0) {
      return []
    }

    // Группируем транзакции по категориям
    const categoryTotals: Record<string, number> = {}
    
    debitTransactions.value.forEach((tx: any) => {
      if (!tx.category || !props.categories) return
      
      const categoryId = String(tx.category)
      const amount = tx.debitSize || 0
      
      // Проверяем, что категория существует
      const category = props.categories.find((c: any) => String(c.id) === categoryId)
      
      if (category) {
        if (!categoryTotals[categoryId]) {
          categoryTotals[categoryId] = 0
        }
        categoryTotals[categoryId] += amount
      }
    })

    // Преобразуем в массив и сортируем
    const sortedData = Object.entries(categoryTotals)
      .map(([id, total]) => {
        const category = props.categories.find((c: any) => String(c.id) === id)
        return {
          name: category ? category.name : 'Unknown',
          value: total,
          id: id
        }
      })
      .sort((a, b) => b.value - a.value)

    // Объединяем мелкие категории в "Others" если их больше 5
    if (sortedData.length > 5) {
      const top5 = sortedData.slice(0, 5)
      const othersTotal = sortedData.slice(5).reduce((sum, item) => sum + item.value, 0)
      
      // Проверяем, стоит ли объединять в Others (если сумма меньше 10% от общей)
      if (othersTotal > 0) {
        top5.push({
          name: 'Others',
          value: othersTotal,
          id: 'others'
        })
      }
      
      return top5
    }

    return sortedData
  })

  const chartLabels = computed(() => {
    if (!processedData.value || processedData.value.length === 0) return ['No data']
    return processedData.value.map(item => item.name)
  })

  const chartData = computed(() => ({
    labels: chartLabels.value,
    datasets: [{
      data: processedData.value.map(item => item.value),
      backgroundColor: [
        'rgba(239, 68, 68, 0.8)',   // Red (expenses)
        'rgba(245, 158, 11, 0.8)',  // Orange
        'rgba(236, 72, 153, 0.8)',  // Pink
        'rgba(168, 85, 247, 0.8)',  // Purple
        'rgba(34, 197, 94, 0.8)',   // Green
        'rgba(59, 130, 246, 0.8)',  // Blue
      ],
      borderColor: [
        'rgb(239, 68, 68)',
        'rgb(245, 158, 11)',
        'rgb(236, 72, 153)',
        'rgb(168, 85, 247)',
        'rgb(34, 197, 94)',
        'rgb(59, 130, 246)',
      ],
      borderWidth: 1,
      hoverOffset: 4
    }]
  }))

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: window.innerWidth < 640 ? 1 : 2,
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
            return `${value.toLocaleString('ru-RU', { minimumFractionDigits: 2 })} RUB (${percentage}%)`;
          }
        }
      }
    },
    layout: {
      padding: window.innerWidth < 640 ? 5 : 10
    }
  }

  const total = computed(() => debitTransactions.value.reduce((sum, tx) => sum + (tx.debitSize || 0), 0))
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
        </svg>
        <p class="text-sm">No expense data</p>
      </div>
    </div>

    <!-- Total expenses overlay -->
    <div v-if="processedData.value.length > 0" class="absolute top-4 right-4 md:top-6 md:right-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg px-3 py-2 shadow-sm">
      <p class="text-xs text-gray-500 dark:text-gray-400">Total Expenses</p>
      <p class="text-lg md:text-xl font-bold text-red-600 dark:text-red-400">{{ total.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} RUB</p>
    </div>

    <!-- Legend for mobile - show below chart -->
    <div v-if="processedData.value.length > 0 && window.innerWidth < 640" class="mt-3 px-2">
      <div class="grid grid-cols-3 gap-2 text-xs">
        <div v-for="(item, idx) in processedData.value.slice(0, 6)" :key="idx" 
             class="flex items-center gap-1 truncate"
             :title="item.name">
          <span class="w-2 h-2 rounded-full flex-shrink-0" 
                :style="{ backgroundColor: chartOptions.plugins!.legend!['labels']?.generateLabels({data: chartData})[idx]?.fillStyle || chartData.datasets[0].borderColor[idx] }"></span>
          <span class="truncate text-gray-600 dark:text-gray-400">{{ item.name.substring(0, 8) }}</span>
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
