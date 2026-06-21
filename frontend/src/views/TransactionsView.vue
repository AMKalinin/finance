<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { transactionApi } from '@/api/client'
import { accountApi } from '@/api/client'
import { categoryApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const transactions = ref([])
const loading = ref(false)
const error = ref(null)
const accountsMap = ref(new Map())
const categoriesMap = ref(new Map())

const currentPeriod = ref('')
const activeFilter = ref('all')

const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const periodDropdownOpen = ref(false)
const periodOptions = ref([])

// Текущая дата для отображения периода
const now = new Date()
const currentMonth = now.getMonth()
const currentYear = now.getFullYear()

function initPeriodOptions() {
  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ]
  periodOptions.value = []
  for (let y = currentYear - 1; y <= currentYear + 1; y++) {
    for (let m = 0; m < 12; m++) {
      const startDate = `${y}-${String(m + 1).padStart(2, '0')}-01`
      const endDate = new Date(y, m + 1, 0).toISOString().split('T')[0]
      periodOptions.value.push({
        label: `${months[m]} ${y}`,
        startDate,
        endDate,
        key: `${y}-${m}`
      })
    }
  }
  // Установить текущий период по умолчанию
  const current = periodOptions.value.find(p => p.key === `${currentYear}-${currentMonth}`)
  if (current) {
    currentPeriod.value = current.label
  }
}

async function loadTransactions() {
  loading.value = true
  error.value = null
  try {
    // Загружаем счета и категории для маппинга
    const [accountsResp, categoriesResp] = await Promise.all([
      accountApi.getAll(),
      categoryApi.getAll()
    ])
    
    // Обработка ответа от API с разными форматами
    const accountsData = (accountsResp.data?.items || accountsResp.data || [])
    const accounts = accountsData.map(a => ({
      id: a.id,
      name: a.name,
      type: a.type || a.account_type,
      currency: a.currency,
      balance: a.balance
    }))
    accountsMap.value = new Map(accounts.map(a => [a.id, a]))

    const categoriesData = (categoriesResp.data?.items || categoriesResp.data || [])
    // Собираем все категории (корневые + вложенные)
    const allCats = []
    for (const cat of categoriesData) {
      allCats.push(cat)
      const subs = cat.subCategory || cat.children || []
      for (const child of subs) {
        allCats.push(child)
        const gsubs = child.subCategory || child.children || []
        for (const gc of gsubs) {
          allCats.push(gc)
        }
      }
    }
    categoriesMap.value = new Map(allCats.map(c => [c.id, c]))

    const period = periodOptions.value.find(p => p.label === currentPeriod.value)
    const params = {
      skip: (pagination.value.currentPage - 1) * pagination.value.itemsPerPage,
      limit: pagination.value.itemsPerPage
    }

    let response
    if (!period) {
      response = await transactionApi.getAll(params)
    } else if (activeFilter.value !== 'all') {
      response = await transactionApi.getByPeriodWithType(
        period.startDate, period.endDate, activeFilter.value, params
      )
    } else {
      response = await transactionApi.getByPeriod(
        period.startDate, period.endDate, params
      )
    }

    const data = response.data
    const rawItems = data?.items || []

    // Маппинг с accountsMap и categoriesMap
    transactions.value = rawItems.map(txn => transactionApi.mapFromBackend(txn, accountsMap.value, categoriesMap.value))
    pagination.value.totalItems = data?.total || 0
    pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.itemsPerPage)
  } catch (err) {
    console.error('Ошибка загрузки транзакций:', err)
    error.value = err.message || 'Не удалось загрузить транзакции'
    transactions.value = []
  } finally {
    loading.value = false
  }
}

// Сброс на первую страницу при смене периода/фильтра
watch([currentPeriod, activeFilter], () => {
  pagination.value.currentPage = 1
  loadTransactions()
})

function filterTransactions(type) {
  activeFilter.value = type
  pagination.value.currentPage = 1
  loadTransactions()
}

function openEditTransaction(txn) {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'transaction', data: txn } }))
}

function openNewTransactionModal() {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'transaction' } }))
}

async function deleteTransaction(id, name) {
  if (confirm(`Вы уверены, что хотите удалить транзакцию "${name}"?`)) {
    try {
      await transactionApi.delete(id)
      // Удалить из локального списка
      transactions.value = transactions.value.filter(t => t.id !== id)
      pagination.value.totalItems = Math.max(0, pagination.value.totalItems - 1)
      pagination.value.totalPages = Math.ceil(pagination.value.totalItems / pagination.value.itemsPerPage)
      // Если последняя страница пуста, перейти на предыдущую
      if (pagination.value.currentPage > pagination.value.totalPages && pagination.value.totalPages > 0) {
        pagination.value.currentPage--
        loadTransactions()
      }
    } catch (err) {
      console.error('Ошибка удаления транзакции:', err)
      alert('Не удалось удалить транзакцию: ' + (err.message || 'неизвестная ошибка'))
    }
  }
}

const filteredTransactions = computed(() => {
  return transactions.value
})

function formatAmount(amount, currency) {
  if (amount == null) return '₽ 0.00'
  const symbols = { RUB: '₽', USD: '$', EUR: '€' }
  const symbol = symbols[currency] || '₽'
  return `${amount > 0 ? '+' : ''}${symbol} ${Math.abs(amount).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

function formatDateFull(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function getStatusBadge(status) {
  switch (status) {
    case 'settled':
      return '<span class="px-2 py-1 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-xs font-medium">✓</span>'
    case 'pending':
      return '<span class="px-2 py-1 bg-yellow-50 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded-full text-xs font-medium">⏳</span>'
    case 'partially_paid':
      return '<span class="px-2 py-1 bg-orange-50 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 rounded-full text-xs font-medium">🔄</span>'
    default:
      return ''
  }
}

function getIconBg(type) {
  switch (type) {
    case 'debit':
      return 'bg-red-50 dark:bg-red-900/20 text-red-600'
    case 'adding':
      return 'bg-green-50 dark:bg-green-900/20 text-green-600'
    case 'transfer':
      return 'bg-blue-50 dark:bg-blue-900/20 text-blue-600'
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
  }
}

function getCategoryIcon(category) {
  const icons = {
    'food': '🍔', 'transport': '🚗', 'home': '🏠', 'health': '🏥',
    'education': '📚', 'entertainment': '🎮', 'shopping': '🛒',
    'salary': '💼', 'investment': '📈', 'gift': '🎁',
    'default': '📁'
  }
  if (!category) return icons.default
  const name = category.name?.toLowerCase() || ''
  if (name.includes('еда') || name.includes('food')) return icons.food
  if (name.includes('транспорт') || name.includes('transport')) return icons.transport
  if (name.includes('дом') || name.includes('home')) return icons.home
  if (name.includes('здоров') || name.includes('health')) return icons.health
  if (name.includes('образ') || name.includes('education')) return icons.education
  if (name.includes('развлеч') || name.includes('entertain')) return icons.entertainment
  if (name.includes('покупк') || name.includes('shop')) return icons.shopping
  if (name.includes('зарплат') || name.includes('salary')) return icons.salary
  if (name.includes('инвест') || name.includes('invest')) return icons.investment
  if (name.includes('подарок') || name.includes('gift')) return icons.gift
  return icons.default
}

function getPeriodSummary() {
  if (transactions.value.length === 0) return null
  let income = 0
  let expense = 0
  for (const txn of transactions.value) {
    if (txn.amount > 0) income += txn.amount
    else expense += Math.abs(txn.amount)
  }
  return { income, expense, balance: income - expense }
}

function goToPage(page) {
  if (page >= 1 && page <= pagination.value.totalPages) {
    pagination.value.currentPage = page
    loadTransactions()
  }
}

onMounted(() => {
  initPeriodOptions()
  loadTransactions()
  window.addEventListener('modalSaved', handleModalSaved)
})

onUnmounted(() => {
  window.removeEventListener('modalSaved', handleModalSaved)
})

function handleModalSaved(event) {
  if (event.detail?.type === 'transaction') {
    loadTransactions()
  }
}

// Пагинация — вычисляемое свойство в Composition API
const displayedPages = computed(() => {
  const total = pagination.value.totalPages
  const current = pagination.value.currentPage
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  const pages = []
  pages.push(1)
  if (current > 3) pages.push('...')
  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
    pages.push(i)
  }
  if (current < total - 2) pages.push('...')
  pages.push(total)
  return pages
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ t("nav.transactions") }}</h1>
      <button @click="openNewTransactionModal" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
        ➕ {{ t("actions.createTransaction") }}
      </button>
    </div>

    <!-- Period Selector -->
    <div class="flex flex-wrap items-center gap-4">
      <div class="relative">
        <button
          @click="periodDropdownOpen = !periodDropdownOpen"
          class="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center gap-2"
        >
          📅 {{ currentPeriod }}
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-if="periodDropdownOpen" class="absolute top-full left-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto w-48">
          <div class="p-2 text-xs text-gray-500 dark:text-gray-400 font-medium border-b border-gray-200 dark:border-gray-700">Год {{ currentYear }}</div>
          <button
            v-for="period in periodOptions.filter(p => p.key.startsWith(`${currentYear}-`))"
            :key="period.key"
            @click="currentPeriod = period.label; periodDropdownOpen = false"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            :class="currentPeriod === period.label ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-700 dark:text-gray-300'"
          >
            {{ period.label }}
          </button>
          <div class="p-2 text-xs text-gray-500 dark:text-gray-400 font-medium border-t border-gray-200 dark:border-gray-700">Год {{ currentYear + 1 }}</div>
          <button
            v-for="period in periodOptions.filter(p => p.key.startsWith(`${currentYear + 1}-`))"
            :key="period.key"
            @click="currentPeriod = period.label; periodDropdownOpen = false"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            :class="currentPeriod === period.label ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium' : 'text-gray-700 dark:text-gray-300'"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-2">
      <button
        @click="filterTransactions('all')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
          activeFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
        ]">
        {{ t('common.allTypes') }}
      </button>
      <button
        @click="filterTransactions('debit')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
          activeFilter === 'debit' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
        ]">
        {{ t('common.expenses') }}
      </button>
      <button
        @click="filterTransactions('adding')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
          activeFilter === 'adding' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
        ]">
        {{ t('common.income') }}
      </button>
      <button
        @click="filterTransactions('transfer')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
          activeFilter === 'transfer' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
        ]">
        {{ t('common.transfers') }}
      </button>
    </div>

    <!-- Period Summary -->
    <div v-if="!loading && !error && transactions.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
        <p class="text-sm text-gray-500 dark:text-gray-400">Доходы</p>
        <p class="text-xl font-bold text-green-600">{{ formatAmount(getPeriodSummary().income, 'RUB') }}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
        <p class="text-sm text-gray-500 dark:text-gray-400">Расходы</p>
        <p class="text-xl font-bold text-red-600">-{{ formatAmount(getPeriodSummary().expense, 'RUB') }}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700">
        <p class="text-sm text-gray-500 dark:text-gray-400">Баланс</p>
        <p class="text-xl font-bold" :class="getPeriodSummary().balance >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ formatAmount(getPeriodSummary().balance, 'RUB') }}
        </p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="flex items-center gap-3 text-gray-500">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Загрузка транзакций...</span>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-4 rounded-lg text-red-700 dark:text-red-400">
      <p class="font-medium">Ошибка загрузки</p>
      <p class="text-sm">{{ error }}</p>
      <button @click="loadTransactions" class="mt-2 text-sm underline hover:no-underline">Попробовать снова</button>
    </div>

    <!-- Transactions List -->
    <div v-else-if="filteredTransactions.length > 0" class="space-y-2">
      <div v-for="txn in filteredTransactions" :key="txn.id" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow group">
        <div class="flex items-center gap-4">
          <!-- Icon -->
          <div class="w-11 h-11 rounded-lg flex items-center justify-center text-xl" :class="getIconBg(txn.type)">
            {{ getCategoryIcon(txn.category) }}
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <h3 class="font-medium text-gray-900 dark:text-gray-100 truncate">{{ txn.name || txn.description || 'Без описания' }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
              <span v-if="txn.category?.name">📁 {{ txn.category.name }}</span>
              <span v-if="txn.category?.name && txn.account?.name"> | </span>
              <span v-if="txn.account?.name">💳 {{ txn.account.name }}</span>
            </p>
            <!-- Positions -->
            <div v-if="txn.positions && txn.positions.length > 0" class="mt-1 flex flex-wrap gap-1">
              <span
                v-for="pos in txn.positions"
                :key="pos.id || pos.name"
                class="inline-flex items-center gap-1 px-2 py-0.5 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400 rounded text-xs font-medium"
              >
                📊 {{ pos.name }}
                <span class="text-purple-500 dark:text-purple-500">×{{ pos.quantity }}</span>
              </span>
            </div>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
              {{ formatDateFull(txn.date) }}
            </p>
          </div>

          <!-- Status Badge -->
          <div v-html="getStatusBadge(txn.status)"></div>

          <!-- Amount -->
          <div :class="[
            'font-mono font-semibold text-lg whitespace-nowrap',
            txn.amount >= 0 ? 'text-green-600' : 'text-red-500'
          ]">
            {{ formatAmount(txn.amount, txn.currency) }}
          </div>

          <!-- Actions (hover only on desktop) -->
          <div class="hidden sm:flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button @click="openEditTransaction(txn)" class="p-1.5 bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-200 dark:hover:bg-blue-900/50 text-blue-600 rounded transition-colors" title="Редактировать">
              ✏️
            </button>
            <button @click="deleteTransaction(txn.id, txn.name || txn.description || 'транзакцию')" class="p-1.5 bg-red-100 dark:bg-red-900/30 hover:bg-red-200 dark:hover:bg-red-900/50 text-red-600 rounded transition-colors" title="Удалить">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400 py-4">Нет транзакций для отображения</p>
      <button @click="openNewTransactionModal" class="mt-2 text-blue-600 hover:underline text-sm">Создать первую транзакцию</button>
    </div>

    <!-- Pagination -->
    <div v-if="pagination.totalPages > 1" class="flex items-center justify-center gap-2 pt-4">
      <button
        @click="goToPage(1)"
        :disabled="pagination.currentPage === 1"
        class="w-9 h-9 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 flex items-center justify-center text-sm font-medium disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        ←
      </button>

      <template v-for="page in displayedPages" :key="page">
        <button
          v-if="page !== '...'"
          @click="goToPage(page)"
          :class="[
            'w-9 h-9 rounded-lg font-medium text-sm transition-colors',
            page === pagination.currentPage
              ? 'bg-blue-600 text-white border-transparent'
              : 'border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400'
          ]"
        >
          {{ page }}
        </button>
        <span v-else class="px-1 text-gray-600 dark:text-gray-400">...</span>
      </template>

      <button
        @click="goToPage(pagination.totalPages)"
        :disabled="pagination.currentPage === pagination.totalPages"
        class="w-9 h-9 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 flex items-center justify-center text-sm font-medium disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        →
      </button>

      <span class="text-sm text-gray-600 dark:text-gray-400 ml-2">
        {{ t('common.page') }} {{ pagination.currentPage }} {{ t('common.of') }} {{ pagination.totalPages }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.group:hover .opacity-100 {
  opacity: 1;
}
</style>
