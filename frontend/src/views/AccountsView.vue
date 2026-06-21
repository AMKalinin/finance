<script setup>
import { ref, computed, onMounted } from 'vue'
import { accountApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const accounts = ref([])
const archivedAccounts = ref([])
const isLoading = ref(true)
const showArchived = ref(false)
const searchQuery = ref('')

onMounted(async () => {
  await fetchAccounts()
  await fetchArchivedAccounts()
})

async function fetchAccounts() {
  try {
    const response = await accountApi.getAll({ skip: 0, limit: 1000 })
    const items = response.data?.items || response.data?.accounts || []
    accounts.value = items.map(accountApi.mapFromBackend)
  } catch (error) {
    console.error('Failed to fetch accounts:', error)
    accounts.value = []
  } finally {
    isLoading.value = false
  }
}

async function fetchArchivedAccounts() {
  try {
    const response = await accountApi.archived({ skip: 0, limit: 1000 })
    const items = response.data?.items || response.data?.accounts || []
    archivedAccounts.value = items.map(accountApi.mapFromBackend)
  } catch (error) {
    console.error('Failed to fetch archived accounts:', error)
    archivedAccounts.value = []
  }
}

function formatAmount(amount, currency) {
  const symbols = { RUB: '₽', USD: '$', EUR: '€' }
  const symbol = symbols[currency] || '₽'
  const formatted = Math.abs(amount).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  return `${symbol} ${amount < 0 ? '-' : ''}${formatted}`
}

function getBalanceClass(amount) {
  if (amount < 0) return 'text-red-500'
  if (amount > 0) return 'text-green-600'
  return 'text-gray-900 dark:text-gray-100'
}

function openEditAccount(account) {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'account', data: account } }))
}

function openNewAccountModal() {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'account' } }))
}

async function archiveAccount(account) {
  try {
    await accountApi.archive(account.id)
    accounts.value = accounts.value.filter(a => a.id !== account.id)
    archivedAccounts.value = [...archivedAccounts.value, accountApi.mapFromBackend({
      id: account.id,
      name: account.name,
      type: account.type,
      currency: account.currency,
      balance: account.balance,
      description: account.description,
      interestRate: account.interestRate,
      isPrimary: account.isPrimary,
      archived: true,
    })]
  } catch (error) {
    console.error('Failed to archive account:', error)
  }
}

async function restoreAccount(account) {
  try {
    await accountApi.restore(account.id)
    archivedAccounts.value = archivedAccounts.value.filter(a => a.id !== account.id)
    accounts.value = [...accounts.value, accountApi.mapFromBackend({
      id: account.id,
      name: account.name,
      type: account.type,
      currency: account.currency,
      balance: account.balance,
      description: account.description,
      interestRate: account.interestRate,
      isPrimary: account.isPrimary,
      archived: false,
    })]
  } catch (error) {
    console.error('Failed to restore account:', error)
  }
}

async function deleteAccount(account) {
  if (confirm(`Вы уверены, что хотите удалить счет "${account.name}"?`)) {
    try {
      await accountApi.delete(account.id)
      accounts.value = accounts.value.filter(a => a.id !== account.id)
    } catch (error) {
      console.error('Failed to delete account:', error)
    }
  }
}

const filteredAccounts = computed(() => {
  let filtered = showArchived.value
    ? archivedAccounts.value
    : accounts.value.filter(a => !a.archived)

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(a =>
      a.name?.toLowerCase().includes(query) ||
      a.type?.toLowerCase().includes(query) ||
      a.currency?.toLowerCase().includes(query)
    )
  }

  return filtered
})

function getAccountIcon(type) {
  const icons = {
    debit: '💳',
    credit: '🏦',
    cash: '💵',
    investment: '📈',
    savings: '🏦',
  }
  return icons[type] || '💰'
}

function getAccountGradient(type) {
  const gradients = {
    debit: 'from-blue-500 to-blue-600',
    credit: 'from-purple-500 to-purple-600',
    cash: 'from-green-500 to-green-600',
    investment: 'from-orange-500 to-orange-600',
    savings: 'from-teal-500 to-teal-600',
  }
  return gradients[type] || 'from-gray-500 to-gray-600'
}

const totalBalance = computed(() => {
  return accounts.value
    .reduce((sum, a) => sum + (parseFloat(a.balance) || 0), 0)
    .toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
})

const activeAccountsCount = computed(() => {
  return accounts.value.filter(a => !a.archived).length
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">💰 Мои счета</h1>
      <button @click="openNewAccountModal" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
        ➕ {{ t("actions.newAccount") }}
      </button>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-6 text-white">
        <p class="text-sm font-medium text-blue-100">{{ t('common.activeAccounts') }}</p>
        <p class="text-3xl font-bold mt-1">{{ activeAccountsCount }}</p>
      </div>
      <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white">
        <p class="text-sm font-medium text-green-100">{{ t('common.totalBalance') }}</p>
        <p class="text-3xl font-bold mt-1">₽ {{ totalBalance }}</p>
      </div>
    </div>

    <!-- Search -->
    <div class="relative">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input
        type="text"
        v-model="searchQuery"
        :placeholder="t('common.searchAccounts')"
        class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      />
    </div>

    <!-- Tabs -->
    <div class="flex gap-2 border-b border-gray-200 dark:border-gray-700">
      <button
        @click="showArchived = false"
        :class="[
          'px-4 py-2 font-medium text-sm rounded-t-lg transition-colors',
          !showArchived
            ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
        ]">
        Активные ({{ accounts.filter(a => !a.archived).length }})
      </button>
      <button
        @click="showArchived = true"
        :class="[
          'px-4 py-2 font-medium text-sm rounded-t-lg transition-colors',
          showArchived
            ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
        ]">
        Архив ({{ archivedAccounts.length }})
      </button>
    </div>

    <!-- Accounts Grid -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="bg-white dark:bg-gray-800 rounded-xl p-6 animate-pulse border border-gray-200 dark:border-gray-700">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-3"></div>
        <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-4"></div>
        <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
        <div class="flex gap-2">
          <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
          <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
        </div>
      </div>
    </div>

    <template v-else-if="filteredAccounts.length > 0">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="account in filteredAccounts"
          :key="account.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 relative hover:shadow-md transition-shadow group"
        >
          <!-- Primary Badge -->
          <div v-if="account.isPrimary" class="absolute top-4 right-4 text-yellow-500 text-xl">⭐</div>

          <!-- Account Type Icon -->
          <div class="w-12 h-12 rounded-lg bg-gradient-to-br flex items-center justify-center text-2xl mb-4"
            :class="getAccountGradient(account.type)">
            {{ getAccountIcon(account.type) }}
          </div>

          <!-- Account Type -->
          <span class="text-xs uppercase tracking-wider font-semibold text-gray-500 dark:text-gray-400">{{ account.type }}</span>

          <!-- Account Name -->
          <h3 class="font-semibold text-lg text-gray-900 dark:text-gray-100 mt-1 mb-2">{{ account.name }}</h3>

          <!-- Balance -->
          <div class="text-2xl font-mono font-bold my-3" :class="getBalanceClass(account.balance)">
            {{ formatAmount(account.balance, account.currency) }}
          </div>

          <!-- Interest Rate -->
          <div v-if="account.interestRate" class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            {{ t("common.interestRate") }} {{ account.interestRate }}%
          </div>

          <!-- Currency Badge -->
          <div class="flex items-center gap-2 mt-2">
            <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded text-xs font-medium">
              {{ account.currency }}
            </span>
          </div>

          <!-- Actions -->
          <div class="flex flex-wrap gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
            <button
              @click="openEditAccount(account)"
              class="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-200 dark:hover:bg-blue-900/50 text-blue-600 rounded-lg text-sm transition-colors flex items-center gap-1"
            >
              ✏️ {{ t("common.edit") }}
            </button>
            <button
              @click="archiveAccount(account)"
              class="px-3 py-1 bg-yellow-50 dark:bg-yellow-900/30 hover:bg-yellow-100 dark:hover:bg-yellow-900/50 text-yellow-600 rounded-lg text-sm transition-colors flex items-center gap-1"
            >
              📦 {{ t("common.archive") }}
            </button>
            <button
              @click="deleteAccount(account)"
              class="px-3 py-1 bg-red-50 dark:bg-red-900/30 hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 rounded-lg text-sm transition-colors flex items-center gap-1"
            >
              🗑️ {{ t("common.delete") }}
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State for search -->
      <template v-if="searchQuery && filteredAccounts.length === 0">
        <p class="text-center text-gray-500 dark:text-gray-400 py-12">
          По запросу "{{ searchQuery }}" ничего не найдено
        </p>
      </template>

      <!-- Empty State for active accounts -->
      <template v-if="!showArchived && accounts.length === 0">
        <p class="text-center text-gray-500 dark:text-gray-400 py-12">
          Нет активных счетов. Создайте первый!
        </p>
      </template>

      <!-- Empty State for archived accounts -->
      <template v-if="showArchived && archivedAccounts.length === 0">
        <p class="text-center text-gray-500 dark:text-gray-400 py-12">
          Архив пуст
        </p>
      </template>
    </template>

    <!-- Empty State -->
    <div v-else-if="!isLoading" class="text-center text-gray-500 dark:text-gray-400 py-12">
      Нет счетов. Создайте первый!
    </div>
  </div>
</template>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .7; }
}
</style>
