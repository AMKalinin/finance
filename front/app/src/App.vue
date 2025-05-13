<script setup lang="ts">
  import { RouterLink, RouterView} from 'vue-router'
  import router from './router/router'
  import { ref, onMounted } from 'vue'
  import SideBar from './components/SideBar.vue'
  import MyHeader from './components/MyHeader.vue'

  import { getKeycloak, getUserInfo } from './keycloak/keycloak.js'
  import { finApi } from './api/finApi.js'

  const currentTab = ref('overview')
  const userName = ref('')

  const handleTabChange = (tab: string) => {
    currentTab.value = tab
    let st = '/' + tab
    router.push(st)
  }

  const accounts = ref([])

  const categories = ref([])

  const transactions = ref([])

  const addAccount = async (account: any) => {
    try {
      const accountResp = await finApi.createAccount(account)
      accounts.value.push(accountResp)
    } catch (error) {
      console.error('Не удалось создать счет:', error);
    }
  }

  const deleteAccount = async (accountId: number) => {
    // Simulate API call
    // await new Promise(resolve => setTimeout(resolve, 300))
    accounts.value = accounts.value.filter(acc => acc.id !== accountId)
  }

  const addCategory = async (category: any) => {
    if (category.type === 'expense'){
      category.type = 'Debit'
    } else{
      category.type = 'Credit'
    }
    try {
      const categoryResp = await finApi.createCategory(category)
      categories.value.push(categoryResp)
    } catch (error) {
      console.error('Не удалось создать категорию:', error);
    }
  }

  const deleteCategory = async (categoryInfo: object) => {
    // Simulate API call
    // await new Promise(resolve => setTimeout(resolve, 300))
    let catId = categoryInfo.categoryId
    categories.value = categories.value.filter(cat => cat.id !== catId)
  }

  const addTransaction = async (transaction: any) => {
    try {
      await finApi.createTransaction(transaction)
      transactions.value.push(transaction)
      await fetchAccounts()
    } catch (error) {
      console.error('Не удалось создать транзакцию:', error);
    }
  }

  const deleteTransaction = async (transactionId: number) => {
    // Simulate API call
    // await new Promise(resolve => setTimeout(resolve, 300))
    transactions.value = transactions.value.filter(transac => transac.id !== transactionId)
  }


  async function fetchAccounts() {
    try {
      accounts.value = await finApi.getAccounts()
    } catch (error) {
      console.error('Не удалось загрузить счета:', error);
    }
  }

  async function fetchCategory() {
    try {
      categories.value = await finApi.getCategories()
    } catch (error) {
      console.error('Не удалось загрузить :', error);
    }
  }

  async function fetchTransactions() {
    try {
      transactions.value = await finApi.getTransactions()
      transactions.value = transactions.value.sort((a, b) => new Date(b.date) - new Date(a.date))
    } catch (error) {
      console.error('Не удалось загрузить :', error);
    }
  }

  onMounted(() => {
    fetchAccounts()
    fetchCategory()
    fetchTransactions()
  })

</script>

<template>
  <div class="flex min-h-screen bg-main">
    <SideBar class="fixed left-0 top-0" @tab-change="handleTabChange"/>
    <main class="flex-1 p-8 ml-20">
      <MyHeader :currentTab="currentTab" :userName="getUserInfo().email"/>
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
</style>
