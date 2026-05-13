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
  <!-- Charts Section - Stack on mobile, side by side on larger screens -->
  <div :class="[
    'grid gap-4 lg:gap-6 mb-6 lg:mb-8',
    'md:grid-cols-2'
  ]">

    <!-- Portfolio Chart Card -->
    <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white">Account Distribution</h2>
          <p class="text-xs md:text-sm text-gray-500 dark:text-gray-400">Balance allocation</p>
        </div>
      </div>
      <PortfolioChart :accounts="accounts"/>
    </div>

    <!-- Category Chart Card -->
    <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white">Category Distribution</h2>
          <p class="text-xs md:text-sm text-gray-500 dark:text-gray-400">Spending breakdown</p>
        </div>
      </div>
      <CategoryChart
        :transactions="transactions"
        :categories="categories"
      />
    </div>
  </div>

  <!-- Cards Section - Responsive grid -->
  <div :class="[
    'grid gap-4 lg:gap-6',
    'md:grid-cols-2 xl:grid-cols-3'
  ]">
    
    <!-- Top Accounts -->
    <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white mb-4">Top Accounts</h2>
      <TopAccounts
        :accounts="accounts"
        @add-account="$emit('addAccount', $event)"
        @delete-account="$emit('deleteAccount', $event)"
      />
    </div>

    <!-- Top Categories -->
    <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white mb-4">Top Categories</h2>
      <TopCategories
        :categories="categories"
        @add-category="$emit('addCategory', $event)"
        @delete-category="$emit('deleteCategory', $event)"
      />
    </div>

    <!-- Recent Transactions -->
    <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white mb-4">Recent Transactions</h2>
      <TransactionTable
        :transactions="transactions"
        :categories="categories"
        :accounts="accounts"
        @add-transaction="$emit('addTransaction', $event)"
        @delete-transaction="$emit('deleteTransaction', $event)"
      />
    </div>

  </div>

</template>

<style scoped>
  /* Custom scrollbar */
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.2);
  }
</style>
