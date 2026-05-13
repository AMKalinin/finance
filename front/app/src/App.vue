<script setup lang="ts">
  import { RouterLink, RouterView} from 'vue-router'
  import router from './router/router'
  import { ref, onMounted, onUnmounted } from 'vue'
  import SideBar from './components/SideBar.vue'
  import MyHeader from './components/MyHeader.vue'

  import { getKeycloak, getUserInfo } from './keycloak/keycloak.js'
  import { finApi } from './api/finApi.js'
  import {
    HomeIcon,
    WalletIcon,
    ChartPieIcon,
    ArrowsRightLeftIcon,
    UserIcon,
    Cog6ToothIcon
  } from '@heroicons/vue/24/outline'

  const currentTab = ref('overview')
  const userName = ref('')
  const isMobile = ref(false)
  const mobileMenuOpen = ref(false)

  // Меню для навигации
  const menuItems = [
    { name: 'Overview', icon: HomeIcon, id: 'overview' },
    { name: 'Accounts', icon: WalletIcon, id: 'accounts' },
    { name: 'Categories', icon: ChartPieIcon, id: 'categories' },
    { name: 'Transactions', icon: ArrowsRightLeftIcon, id: 'transactions' },
    { name: 'Profile', icon: UserIcon, id: 'profile' },
  ]

  const handleTabChange = (tab: string) => {
    currentTab.value = tab
    let st = '/' + tab
    router.push(st)
  }

  // Проверка размера экрана
  const checkMobile = () => {
    isMobile.value = window.innerWidth < 1024
  }

  const toggleMobileMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value
  }

  const accounts = ref<any[]>([])
  const categories = ref<any[]>([])
  const transactions = ref<any[]>([])

  const addAccount = async (account: any) => {
    try {
      const accountResp = await finApi.createAccount(account)
      accounts.value.push(accountResp)
    } catch (error) {
      console.error('Не удалось создать счет:', error);
    }
  }

  const deleteAccount = async (accountId: string) => {
    try {
      await finApi.deleteAccount(accountId)
      accounts.value = accounts.value.filter(acc => String(acc.id) !== accountId)
    } catch (error) {
      console.error('Не удалось удалить счет:', error);
    }
  }

  const addCategory = async (category: any) => {
    try {
      const categoryResp = await finApi.createCategory(category)
      categories.value.push(categoryResp)
    } catch (error) {
      console.error('Не удалось создать категорию:', error);
    }
  }

  const deleteCategory = async (categoryId: string) => {
    try {
      await finApi.deleteCategory(categoryId)
      categories.value = categories.value.filter(cat => String(cat.id) !== categoryId)
    } catch (error) {
      console.error('Не удалось удалить категорию:', error);
    }
  }

  const addTransaction = async (transaction: any) => {
    try {
      await finApi.createTransaction(transaction)
      transactions.value.unshift(transaction)
      await fetchAccounts()
    } catch (error) {
      console.error('Не удалось создать транзацию:', error);
    }
  }

  const deleteTransaction = async (transactionId: string) => {
    try {
      await finApi.deleteTransaction(transactionId)
      transactions.value = transactions.value.filter(transac => String(transac.id) !== transactionId)
    } catch (error) {
      console.error('Не удалось удалить транзакцию:', error);
    }
  }

  async function fetchAccounts() {
    try {
      const response = await finApi.getAccounts(0, 100)
      accounts.value = Array.isArray(response.items) ? response.items : []
    } catch (error) {
      console.error('Не удалось загрузить счета:', error);
    }
  }

  async function fetchCategories() {
    try {
      const expenseResponse = await finApi.getExpenseCategories(0, 100)
      const incomeResponse = await finApi.getIncomeCategories(0, 100)
      categories.value = [...(expenseResponse.items || []), ...(incomeResponse.items || [])]
    } catch (error) {
      console.error('Не удалось загрузить категории:', error);
    }
  }

  async function fetchTransactions() {
    try {
      const response = await finApi.getTransactions(0, 50)
      transactions.value = Array.isArray(response.items) ? response.items.sort((a, b) => new Date(b.date) - new Date(a.date)) : []
    } catch (error) {
      console.error('Не удалось загрузить транзакции:', error);
    }
  }

  onMounted(() => {
    fetchAccounts()
    fetchCategories()
    fetchTransactions()
    checkMobile()
    window.addEventListener('resize', checkMobile)
  })

  // Очистка слушателя событий при размонтировании
  onUnmounted(() => {
    window.removeEventListener('resize', checkMobile)
  })
</script>

<template>
  <div class="flex min-h-screen bg-main dark:bg-gray-900">
    <!-- Mobile Bottom Navigation -->
    <nav v-if="isMobile" class="fixed bottom-0 left-0 right-0 bg-surface border-t border-gray-200 dark:bg-gray-800 dark:border-gray-700 z-40 lg:hidden">
      <div class="flex justify-around items-center py-2 px-1">
        <button
          v-for="item in menuItems"
          :key="item.id"
          @click="handleTabChange(item.id)"
          :class="[
            'flex flex-col items-center justify-center py-2 px-3 rounded-lg transition-colors',
            currentTab === item.id ? 'text-primary bg-purple-50 dark:bg-purple-900/30' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          ]"
        >
          <component
            :is="item.icon"
            class="w-6 h-6 mb-1"
          />
          <span class="text-xs font-medium">{{ item.name }}</span>
        </button>
      </div>
    </nav>

    <!-- Desktop Sidebar -->
    <SideBar v-if="!isMobile" class="hidden lg:block fixed left-0 top-0 h-screen z-10" @tab-change="handleTabChange"/>

    <!-- Main Content -->
    <main class="flex-1 transition-all duration-300 lg:ml-[256px] relative z-20">
      <MyHeader 
        :currentTab="currentTab" 
        :userName="getUserInfo().email"
        :showMenuButton="isMobile"
        @menu-click="toggleMobileMenu"
      />

      <!-- Mobile Menu Overlay -->
      <div v-if="mobileMenuOpen && isMobile" class="fixed inset-0 bg-black/50 z-40 lg:hidden" @click="mobileMenuOpen = false"></div>

      <!-- Desktop Sidebar (hidden on mobile) -->
      <aside v-if="isMobile && mobileMenuOpen" class="fixed left-0 top-0 bottom-0 w-64 bg-surface dark:bg-gray-800 z-50 lg:hidden shadow-xl">
        <div class="p-4 border-b dark:border-gray-700">
          <button @click="mobileMenuOpen = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            ← Back
          </button>
        </div>
        <nav class="p-4 space-y-2">
          <button
            v-for="item in menuItems"
            :key="item.id"
            @click="handleTabChange(item.id); mobileMenuOpen = false"
            :class="[
              'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors w-full',
              currentTab === item.id ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700'
            ]"
          >
            <component
              :is="item.icon"
              class="w-5 h-5"
            />
            <span class="font-medium">{{ item.name }}</span>
          </button>
        </nav>
      </aside>

      <RouterView
        :accounts="accounts"
        :categories="categories"
        :transactions="transactions"
        @add-account="addAccount"
        @delete-account="deleteAccount"
        @add-category="addCategory"
        @delete-category="deleteCategory"
        @add-transaction="addTransaction"
        @delete-transaction="deleteTransaction"
      />
    </main>
  </div>
</template>

<style>
  body {
    margin: 0;
    font-family: 'Inter', sans-serif;
  }
  main {
    background-color: #F4F4F4 !important;
  }
  .dark main {
    background-color: #111827 !important;
  }
</style>
