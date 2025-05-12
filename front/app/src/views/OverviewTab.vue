<script setup lang="ts">

  import PortfolioChart from '@/components/PortfolioChart.vue'
  import CategoryChart from '@/components/CategoryChart.vue'
  import TransactionTable from '@/components/TransactionTable.vue'
  import TopAccounts from '@/components/TopAccounts.vue'
  import TopCategories from '@/components/TopCategories.vue'

  const emit = defineEmits([
        'addAccount', 'deleteAccount',
        'addCategory', 'deleteCategory',
        'addTransaction', 'deleteTransaction'
        ])

  const props = defineProps<{
    accounts: any[],
    categories: any[],
    transactions: any[]
  }>()

</script>


<template>

  <div class="grid grid-cols-4 gap-6 mb-8">

    <div class="col-span-2 bg-white p-6 rounded-xl relative">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-2xl font-bold">Account Distribution</h2>
          <p class="text-gray-500">Balance allocation</p>
        </div>
      </div>
      <PortfolioChart :accounts="accounts"/>
    </div>

    <div class="col-span-2 bg-white p-6 rounded-xl relative">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-2xl font-bold">Category Distribution</h2>
          <p class="text-gray-500">Spending breakdown</p>
        </div>
      </div>
      <CategoryChart
        :transactions="transactions"
        :categories="categories"
      />
    </div>
  </div>

  <div class="grid grid-cols-3 gap-6">
    <TopAccounts
      :accounts="accounts"
      @add-account="$emit('addAccount', $event)"
      @delete-account="$emit('deleteAccount', $event)"
    />
    <TopCategories
      :categories="categories"
      @add-category="$emit('addCategory', $event)"
      @delete-category="$emit('deleteCategory', $event)"
    />
    <TransactionTable
      :transactions="transactions"
      :categories="categories"
      :accounts="accounts"
      @add-transaction="emit('addTransaction', $event)"
      @delete-transaction="emit('deleteTransaction', $event)"
    />
  </div>

</template>


