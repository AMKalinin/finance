<script setup lang="ts">
  import { ref, computed } from 'vue'
  import { PlusIcon, TrashIcon } from '@heroicons/vue/24/outline'

  const emit = defineEmits(['addAccount', 'deleteAccount'])

  const props = defineProps<{
    accounts: any[]
  }>()

  const showNewAccountModal = ref(false)
  const newAccountName = ref('')
  const newAccountBalance = ref(0)
  const newAccountCurrency = ref('RUB')

  const openNewAccountModal = () => {
    showNewAccountModal.value = true
    newAccountName.value = ''
    newAccountBalance.value = 0
    newAccountCurrency.value = 'RUB'
  }

  const createNewAccount = () => {
    if (newAccountName.value) {
      emit('addAccount', {
        name: newAccountName.value,
        balance: newAccountBalance.value,
        currency: newAccountCurrency.value
      })
      showNewAccountModal.value = false
    }
  }

  const deleteAccount = (accountId: string) => {
    emit('deleteAccount', accountId)
  }

  const totalBalance = computed(() => {
    return props.accounts.reduce((sum, acc) => sum + (acc.balance || 0), 0)
  })

  const sortedAccounts = computed(() => {
    return [...props.accounts].sort((a, b) => (b.balance || 0) - (a.balance || 0))
  })
</script>


<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden">
    
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 p-4 border-b dark:border-gray-700">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white">Top Accounts</h2>
      <button
        @click="openNewAccountModal"
        class="flex items-center gap-2 px-3 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150"
      >
        <PlusIcon class="w-5 h-5" />
        <span class="hidden sm:inline">Account</span>
      </button>
    </div>

    <!-- Account List -->
    <div class="p-4 space-y-3">
      
      <div v-if="sortedAccounts.length > 0" class="flex justify-between items-center mb-2 px-1">
        <p class="text-xs text-gray-500 dark:text-gray-400">Total Balance</p>
        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ totalBalance.toLocaleString('ru-RU', { minimumFractionDigits: 2 }) }} RUB</p>
      </div>

      <div v-for="(account, index) in sortedAccounts.slice(0, 5)" :key="account.id" 
           class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors group">
        
        <!-- Account Info -->
        <div class="flex items-center gap-3 flex-1 min-w-0">
          <!-- Rank badge -->
          <span :class="[
            'w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold',
            index === 0 ? 'bg-yellow-400 text-white' :
            index === 1 ? 'bg-gray-400 text-white' :
            index === 2 ? 'bg-orange-400 text-white' :
            'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
          ]">
            {{ index + 1 }}
          </span>

          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ account.name }}</p>
            <p :class="[
              'text-xs',
              index === 0 ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'
            ]">
              {{ (account.balance || 0).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) }} RUB
            </p>
          </div>
        </div>

        <!-- Delete Button (visible on hover) -->
        <button 
          @click="deleteAccount(account.id)"
          class="opacity-0 group-hover:opacity-100 p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all duration-200"
          title="Delete account"
        >
          <TrashIcon class="w-4 h-4" />
        </button>
      </div>

      <!-- Empty state -->
      <div v-if="sortedAccounts.length === 0" class="text-center py-8 px-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 opacity-50 text-gray-400 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
        <p class="text-sm text-gray-500 dark:text-gray-400">No accounts yet</p>
      </div>

    </div>
  </div>

  <!-- New Account Modal -->
  <div v-if="showNewAccountModal" class="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md">
      <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Create New Account</h3>
      
      <div class="space-y-4">
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Name</label>
          <input
            v-model="newAccountName"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="e.g., Main Account"
          />
        </div>

        <!-- Initial Balance -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Initial Balance</label>
          <input
            v-model="newAccountBalance"
            type="number"
            step="0.01"
            min="0"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="0.00"
          />
        </div>

        <!-- Currency -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency</label>
          <select
            v-model="newAccountCurrency"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="RUB">RUB</option>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <button
          @click="showNewAccountModal = false"
          class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          Cancel
        </button>
        <button
          @click="createNewAccount"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!newAccountName || newAccountBalance < 0"
        >
          Create Account
        </button>
      </div>
    </div>
  </div>

</template>

<style scoped>
/* Smooth transitions */
.group:hover .opacity-0 {
  opacity: 1 !important;
}
</style>
