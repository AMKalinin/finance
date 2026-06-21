<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const emit = defineEmits(['openModal', 'refresh'])

function openCreateTransaction() {
  emit('openModal', 'transaction')
}

async function refreshAccounts() {
  console.log('Refreshing accounts...')
  // Здесь можно добавить логику перезагрузки данных из API
}

// Mock data
const totalBalance = ref(2450350.00)
const balanceChange = ref('+12%')
const accountsSummary = ref([
  { name: 'Основной банковский', balance: 150000.00, currency: 'RUB' },
  { name: 'Наличные', balance: 5000.00, currency: 'RUB' },
  { name: 'Инвестиции', balance: 25000.00, currency: 'USD' },
])

const expensesByCategory = ref([
  { name: t('dashboard.foodDrinks'), percentage: 35, color: 'bg-blue-600' },
  { name: t('dashboard.transport'), percentage: 18, color: 'bg-green-600' },
  { name: t('dashboard.homeUtilities'), percentage: 17, color: 'bg-yellow-500' },
  { name: t('dashboard.entertainment'), percentage: 12, color: 'bg-red-600' },
  { name: t('dashboard.other'), percentage: 18, color: 'bg-blue-400' },
])

const recentTransactions = ref([
  { id: 1, type: 'expense', icon: '🛒', name: 'Супермаркет "Лента"', category: 'Еда и напитки → Супермаркеты', account: 'Основной банковский', amount: -3450.00, date: '2025-05-15' },
  { id: 2, type: 'income', icon: '💼', name: 'Зарплата', category: 'Доходы → Зарплата', account: 'Основной банковский', amount: 85000.00, date: '2025-05-14' },
  { id: 3, type: 'transfer', icon: '📈', name: 'Покупка акций AAPL', category: 'Инвестиции', account: 'Инвестиционный счёт', amount: -15025.00, date: '2025-05-13' },
])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function formatAmount(amount, currency = 'RUB') {
  const symbols = { RUB: '₽', USD: '$', EUR: '€' }
  const symbol = symbols[currency] || '₿'
  return `${amount > 0 ? '+' : ''}${symbol} ${Math.abs(amount).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

function navigateTo(pageName) {
  window.location.hash = `#/${pageName.toLowerCase()}`
}
</script>

<template @refresh="refreshAccounts">
  <div class="space-y-6">
    <!-- Action Buttons -->
    <div class="flex flex-wrap gap-3">
      <button @click="openCreateTransaction" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
        ➕ {{ t('actions.createTransaction') }}
      </button>
      <button @click="$emit('openModal', 'account')" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors flex items-center gap-2">
        🏦 {{ t('actions.addAccount') }}
      </button>
    </div>

    <!-- Dashboard Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <!-- Total Balance Card -->
      <div class="xl:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ t('dashboard.totalBalance') }}</h3>
          <span class="px-3 py-1 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-sm font-medium">▲ {{ balanceChange }} {{ t('common.perMonth') }}</span>
        </div>
        <div class="text-4xl font-bold font-mono text-gray-900 dark:text-gray-100">₿ {{ totalBalance.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      </div>

      <!-- Expenses Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ t('dashboard.expensesMay') }}</h3>
          <button @click="navigateTo('Transactions')" class="text-sm text-blue-600 hover:underline">{{ t('common.moreInfo') }} →</button>
        </div>
        <div class="text-3xl font-bold font-mono text-red-500">₽ -{{ (45230).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      </div>

      <!-- Income Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ t('dashboard.incomeMay') }}</h3>
          <button @click="navigateTo('Transactions')" class="text-sm text-blue-600 hover:underline">{{ t('common.moreInfo') }} →</button>
        </div>
        <div class="text-3xl font-bold font-mono text-green-600">₽ +{{ (125000).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
      </div>

      <!-- My Accounts Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 xl:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ t('dashboard.myAccounts') }}</h3>
          <button @click="navigateTo('Accounts')" class="text-sm text-blue-600 hover:underline">{{ t('nav.accounts') }} →</button>
        </div>
        <div class="space-y-3">
          <div v-for="(account, index) in accountsSummary" :key="index" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ account.name }}</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-gray-100">₽ {{ account.balance.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} <span class="text-xs text-gray-500 dark:text-gray-400">{{ account.currency }}</span></span>
          </div>
        </div>
      </div>

      <!-- Expenses by Category Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 xl:col-span-2">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{{ t('dashboard.expensesByCategory') }}</h3>
        <div class="space-y-4">
          <div v-for="(category, index) in expensesByCategory" :key="index" class="flex items-center gap-4">
            <span class="text-sm text-gray-600 dark:text-gray-400 w-32">{{ category.name }}</span>
            <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
              <div :class="[category.color, 'h-full rounded-full transition-all duration-500']" :style="{ width: `${category.percentage}%` }"></div>
            </div>
            <span class="text-sm font-semibold text-gray-900 dark:text-gray-100 w-12 text-right">{{ category.percentage }}%</span>
          </div>
        </div>
      </div>

      <!-- Recent Transactions Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">📋 Последние транзакции</h3>
        <div class="space-y-3">
          <div v-for="txn in recentTransactions" :key="txn.id" class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer">
            <div :class="[
              'w-10 h-10 rounded-lg flex items-center justify-center text-xl',
              txn.type === 'expense' ? 'bg-red-50 dark:bg-red-900/20 text-red-600' :
              txn.type === 'income' ? 'bg-green-50 dark:bg-green-900/20 text-green-600' :
              'bg-blue-50 dark:bg-blue-900/20 text-blue-600'
            ]">
              {{ txn.icon }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm text-gray-900 dark:text-gray-100 truncate">{{ txn.name }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ txn.category }}</div>
            </div>
            <div :class="[
              'font-mono font-semibold text-sm',
              txn.amount >= 0 ? 'text-green-600' : 'text-red-500'
            ]">
              {{ formatAmount(txn.amount) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">📊 Статистика</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Всего счетов</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100">3</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Транзакций в мае</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100">47</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600 dark:text-gray-400">Категорий</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100">12</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.transition-ring:hover {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}
</style>
