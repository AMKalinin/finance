<script setup lang="ts">
  import { ref, computed } from 'vue'
  import { PlusIcon } from '@heroicons/vue/24/outline'

  const emit = defineEmits([
        'addTransaction', 'deleteTransaction'
        ])

  const props = defineProps<{
    transactions: any[],
    accounts: any[],
    categories: any[],
    showDescription?: boolean
  }>()

  const showNewTransactionModal = ref(false)
  const newTransactionType = ref('Debit')
  const newTransactionAmount = ref('')
  const newTransactionFromAccount = ref('')
  const newTransactionToAccount = ref('')
  const newTransactionCategory = ref('')
  const newTransactionDate = ref(new Date().toISOString().split('T')[0])
  const newTransactionDescription = ref('')

  const openNewTransactionModal = () => {
    showNewTransactionModal.value = true
    newTransactionType.value = 'Debit'
    newTransactionAmount.value = ''
    newTransactionFromAccount.value = ''
    newTransactionToAccount.value = ''
    newTransactionCategory.value = ''
    newTransactionDate.value = new Date().toISOString().split('T')[0]
    newTransactionDescription.value = ''
  }

  const createNewTransaction = () => {
    if (newTransactionAmount.value) {
      const newTransaction: any = {
        type: newTransactionType.value,
        debitSize: parseFloat(newTransactionAmount.value),
        date: newTransactionDate.value,
        description: newTransactionDescription.value,
        exchangeRate: 1
      }

      if (newTransactionType.value === 'Debit') {
        newTransaction.FROM = newTransactionFromAccount.value
        newTransaction.TO = null
        newTransaction.category = parseInt(newTransactionCategory.value)
      } else if (newTransactionType.value === 'Adding') {
        newTransaction.FROM = null
        newTransaction.TO = newTransactionToAccount.value
        newTransaction.category = parseInt(newTransactionCategory.value)
      } else if (newTransactionType.value === 'Transfer') {
        newTransaction.FROM = newTransactionFromAccount.value
        newTransaction.TO = newTransactionToAccount.value
        newTransaction.category = null
      }

      emit('addTransaction', newTransaction)
      showNewTransactionModal.value = false
    }
  }

  const getDebitCategories = computed(() => {
    if (!props.categories) return []
    return props.categories.filter(cat => cat.type === 'Debit' || (Array.isArray(cat.subCategory) && cat.subCategory.some(sub => sub.type === 'Debit')))
  })

  const getCreditCategories = computed(() => {
    if (!props.categories) return []
    return props.categories.filter(cat => cat.type === 'Credit' || (Array.isArray(cat.subCategory) && cat.subCategory.some(sub => sub.type === 'Credit')))
  })

  const getAccountName = (accountId: string) => {
    const account = props.accounts.find(acc => acc.id === accountId)
    return account ? account.name : accountId
  }

  const getCategoryName = (categoryId: number) => {
    const category = props.categories.find(cat => cat.id === categoryId)
    return category ? category.name : categoryId
  }

  const truncateText = (text: string, maxLength: number = 20) => {
    if (!text || text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  const safeTruncate = (value: any, maxLength: number = 15) => {
    if (!value) return ''
    const strValue = String(value)
    if (strValue.length <= maxLength) return strValue
    return strValue.substring(0, maxLength)
  }
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden">
    
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 p-4 border-b dark:border-gray-700">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white">Recent Transactions</h2>
      <button
        @click="openNewTransactionModal"
        class="flex items-center gap-2 px-3 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150"
      >
        <PlusIcon class="w-5 h-5" />
        <span class="hidden sm:inline">Transaction</span>
      </button>
    </div>

    <!-- Table with horizontal scroll on mobile -->
    <div class="overflow-x-auto">
      <table class="w-full min-w-[600px] lg:min-w-0">
        <thead>
          <tr class="text-left text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50">
            <th class="py-3 px-3 sm:px-4 whitespace-nowrap">Type</th>
            <th class="py-3 px-3 sm:px-4 whitespace-nowrap w-[120px] lg:w-auto">Amount</th>
            <th class="py-3 px-3 sm:px-4 whitespace-nowrap hidden md:table-cell">To/From</th>
            <th class="py-3 px-3 sm:px-4 whitespace-nowrap w-[120px] lg:w-auto">Date</th>
            <th class="py-3 px-3 sm:px-4 whitespace-nowrap hidden lg:table-cell">Description</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="tx in transactions.slice(0, 10)" 
            :key="tx.id" 
            class="border-t dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors"
          >
            <!-- Type with icon -->
            <td class="py-3 px-3 sm:px-4">
              <div class="flex items-center gap-2">
                <div :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                  tx.type === 'Debit' ? 'bg-red-100 dark:bg-red-900/30' :
                  tx.type === 'Adding' ? 'bg-green-100 dark:bg-green-900/30' : 'bg-blue-100 dark:bg-blue-900/30'
                ]">
                  <svg v-if="tx.type === 'Debit'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600 dark:text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else-if="tx.type === 'Adding'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600 dark:text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 00-1 1v4H5a1 1 0 100 2h4v4a1 1 0 102 0v-4h4a1 1 0 100-2h-4V4a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span class="font-medium text-sm text-gray-900 dark:text-gray-100">{{ tx.type }}</span>
              </div>
            </td>

            <!-- Amount -->
            <td class="py-3 px-3 sm:px-4">
              <span :class="[
                'font-mono font-medium',
                tx.type === 'Debit' ? 'text-red-600 dark:text-red-400' :
                tx.type === 'Adding' ? 'text-green-600 dark:text-green-400' : 'text-blue-600 dark:text-blue-400'
              ]">
                {{ tx.debitSize?.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} RUB
              </span>
            </td>

            <!-- To/From (hidden on small screens) -->
            <td class="py-3 px-3 sm:px-4 hidden md:table-cell">
              <div class="text-sm text-gray-600 dark:text-gray-400 max-w-[150px] truncate" :title="`${getAccountName(tx.from_account_id)} → ${tx.type === 'Transfer' ? getAccountName(tx.to_account_id) : getCategoryName(tx.category)}`">
                <template v-if="tx.type === 'Transfer'">
                  {{ safeTruncate(getAccountName(tx.from_account_id), 15) }} → {{ safeTruncate(getAccountName(tx.to_account_id), 15) }}
                </template>
                <template v-else-if="tx.type === 'Debit'">
                  {{ safeTruncate(getAccountName(tx.from_account_id), 15) }} → {{ safeTruncate(getCategoryName(tx.category), 15) }}
                </template>
                <template v-else>
                  {{ safeTruncate(getCategoryName(tx.category), 15) }} → {{ safeTruncate(getAccountName(tx.to_account_id), 15) }}
                </template>
              </div>
            </td>

            <!-- Date -->
            <td class="py-3 px-3 sm:px-4">
              <span class="text-sm text-gray-600 dark:text-gray-400">{{ new Date(tx.date).toLocaleDateString('ru-RU') }}</span>
            </td>

            <!-- Description (hidden on mobile) -->
            <td class="py-3 px-3 sm:px-4 hidden lg:table-cell">
              <div class="text-sm text-gray-600 dark:text-gray-400 max-w-[200px] truncate" :title="tx.description">{{ truncateText(tx.description, 30) }}</div>
            </td>

            <!-- Actions (mobile only - show as icon on right side) -->
            <td class="py-3 px-3 sm:px-4 md:hidden">
              <button 
                @click="$emit('deleteTransaction', tx.id)"
                class="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title="Delete transaction"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h12a2 2 0 002-2V6a1 1 0 000-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </td>
          </tr>

          <!-- Empty state -->
          <tr v-if="transactions.length === 0">
            <td colspan="5" class="py-8 px-4 text-center">
              <div class="text-gray-500 dark:text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <p class="text-sm">No transactions yet</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Show more link if there are more than 10 items -->
    <div v-if="transactions.length > 10" class="p-4 border-t dark:border-gray-700 text-center">
      <button 
        @click="$emit('deleteTransaction', 'show-more')"
        class="text-sm text-primary hover:text-purple-700 font-medium transition-colors"
      >
        Show all {{ transactions.length }} transactions →
      </button>
    </div>

  </div>

  <!-- New Transaction Modal -->
  <div v-if="showNewTransactionModal" class="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
      <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Create New Transaction</h3>
      
      <div class="space-y-4">
        <!-- Transaction Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Transaction Type</label>
          <select
            v-model="newTransactionType"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="Debit">Debit</option>
            <option value="Adding">Adding</option>
            <option value="Transfer">Transfer</option>
          </select>
        </div>

        <!-- Amount -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Amount</label>
          <input
            v-model="newTransactionAmount"
            type="number"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Enter amount"
          />
        </div>

        <!-- Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Date</label>
          <input
            v-model="newTransactionDate"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        <!-- Source Account (for Debit and Transfer) -->
        <div v-if="newTransactionType === 'Debit' || newTransactionType === 'Transfer'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">From Account</label>
          <select
            v-model="newTransactionFromAccount"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Select account</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.name }} ({{ account.balance }} {{ account.currency }})
            </option>
          </select>
        </div>

        <!-- Destination Account (for Adding and Transfer) -->
        <div v-if="newTransactionType === 'Adding' || newTransactionType === 'Transfer'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">To Account</label>
          <select
            v-model="newTransactionToAccount"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Select account</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.name }} ({{ account.balance }} {{ account.currency }})
            </option>
          </select>
        </div>

        <!-- Category (for Debit and Adding) -->
        <div v-if="newTransactionType === 'Debit' || newTransactionType === 'Adding'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category</label>
          <select
            v-model="newTransactionCategory"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Select category</option>
            <template v-if="newTransactionType === 'Debit'">
              <option v-for="category in getDebitCategories()" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </template>
            <template v-else>
              <option v-for="category in getCreditCategories()" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </template>
          </select>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
          <input
            v-model="newTransactionDescription"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Enter description"
          />
        </div>
      </div>

      <div class="flex flex-col sm:flex-row justify-end gap-3 mt-6">
        <button
          @click="showNewTransactionModal = false"
          class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          Cancel
        </button>
        <button
          @click="createNewTransaction"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150"
        >
          Create Transaction
        </button>
      </div>
    </div>
  </div>

</template>

<style scoped>
/* Smooth scrolling for modal */
::-webkit-scrollbar {
  width: 6px;
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

/* Dark mode overrides */
.dark .bg-gray-50 {
  background-color: #1f2937;
}
</style>
