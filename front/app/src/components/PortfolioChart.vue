<script setup lang="ts">
  import { computed } from 'vue'
  import { Pie } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'


  ChartJS.register(ArcElement, Tooltip, Legend)

  const props = defineProps<{
    accounts: Account[]
  }>()


  const processedData = computed(() => {
    const sortedAccounts = [...props.accounts].sort((a, b) => b.balance - a.balance)
    const top5 = sortedAccounts.slice(0, 5)
    const others = sortedAccounts.slice(5)

    const othersTotal = others.reduce((sum, acc) => sum + acc.balance, 0)

    if (others.length > 0) {
      top5.push({
        id: -1,
        name: 'Others',
        balance: othersTotal
      })
    }
    return top5
  })

  const chartData = computed(() => ({
    labels: processedData.value.map(acc => acc.name),
    datasets: [{
      data: processedData.value.map(acc => acc.balance),
      backgroundColor: [
        'rgba(147, 51, 234, 0.2)',  // Purple
        'rgba(234, 179, 8, 0.2)',   // Yellow
        'rgba(34, 197, 94, 0.2)',   // Green
        'rgba(59, 130, 246, 0.2)',  // Blue
        'rgba(236, 72, 153, 0.2)',  // Pink
        'rgba(107, 114, 128, 0.2)', // Gray (for Others)
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
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          usePointStyle: true,
          pointStyle: 'circle',
          padding: 20,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const value = context.raw;
            return `$${value.toLocaleString()}`;
          }
        }
      }
    }
  }

  const total = computed(() => props.accounts.reduce((sum, acc) => sum + acc.balance, 0))

</script>

<template>
  <div class="h-48 flex items-center">
    <div class="w-full h-full 6">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
    <div class="absolute top-6 right-6 text-sm text-gray-500">
      Total: ${{ total.toLocaleString() }}
    </div>
  </div>
</template>
