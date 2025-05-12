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
        typeName: newTransactionType.value,
        size: parseFloat(newTransactionAmount.value),
        date: newTransactionDate.value,
        description: newTransactionDescription.value,
        exchange_rate: 0
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

  const getDebitCategories = () => {
    return props.categories.filter(cat => cat.typeCategory === 'Debit')
  }

  const getCreditCategories = () => {
    return props.categories.filter(cat => cat.typeCategory === 'Credit')
  }

  const getAccountName = (accountId: string) => {
    const account = props.accounts.find(acc => acc.id === accountId)
    return account ? account.name : accountId
  }

  const getCategoryName = (categoryId: number) => {
    const category = props.categories.find(cat => cat.id === categoryId)
    return category ? category.name : categoryId
  }
</script>

<template>
  <div class="bg-white rounded-xl p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold">Recent Transactions</h2>
      <button
        @click="openNewTransactionModal"
        class="flex items-center gap-2 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
      >
        <PlusIcon class="w-5 h-5" />
        <span>Transaction</span>
      </button>
    </div>
    <table class="w-full">
      <thead>
        <tr class="text-left text-sm text-gray-500">
          <th class="pb-2">Type</th>
          <th class="pb-2">Amount</th>
          <th class="pb-2">To/From</th>
          <th class="pb-2">Date</th>
          <th v-if="showDescription" class="pb-2">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tx in transactions" :key="tx.id" class="border-t">
          <td class="py-3">
            <div class="flex items-center gap-2">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center',
                tx.typeName === 'Debit' ? 'bg-red-100' :
                tx.typeName === 'Adding' ? 'bg-green-100' : 'bg-blue-100'
              ]">
                <svg v-if="tx.typeName === 'Debit'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <svg v-else-if="tx.typeName === 'Adding'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 00-1 1v4H5a1 1 0 100 2h4v4a1 1 0 102 0v-4h4a1 1 0 100-2h-4V4a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <div class="font-medium">{{ tx.typeName }}</div>
              </div>
            </div>
          </td>
          <td>{{ tx.size }}</td>
          <td class="font-mono text-sm">
            <template v-if="tx.typeName === 'Transfer'">
              {{ getAccountName(tx.FROM) }} → {{ getAccountName(tx.TO) }}
            </template>
            <template v-else-if="tx.typeName === 'Debit'">
              {{ getAccountName(tx.FROM) }} → {{ getCategoryName(tx.category) }}
            </template>
            <template v-else>
              {{ getCategoryName(tx.category) }} → {{ getAccountName(tx.TO) }}
            </template>
          </td>
          <td>{{ new Date(tx.date).toLocaleDateString('ru-RU', {year: 'numeric', month: 'numeric', day: 'numeric'}) }}</td>
          <td v-if="showDescription">{{ tx.description }}</td>
        </tr>
      </tbody>
    </table>

    <!-- New Transaction Modal -->
    <div v-if="showNewTransactionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Create New Transaction</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Transaction Type</label>
            <select
              v-model="newTransactionType"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="Debit">Debit</option>
              <option value="Adding">Adding</option>
              <option value="Transfer">Transfer</option>
            </select>
          </div>

          <!-- Amount -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
            <input
              v-model="newTransactionAmount"
              type="number"
              step="0.01"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter amount"
            />
          </div>

          <!-- Date -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              v-model="newTransactionDate"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>



          <!-- Source Account (for Debit and Transfer) -->
          <div v-if="newTransactionType === 'Debit' || newTransactionType === 'Transfer'">
            <label class="block text-sm font-medium text-gray-700 mb-1">From Account</label>
            <select
              v-model="newTransactionFromAccount"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">Select account</option>
              <option v-for="account in accounts" :key="account.id" :value="account.id">
                {{ account.name }} ({{ account.balance }} {{ account.currency }})
              </option>
            </select>
          </div>

          <!-- Destination Account (for Adding and Transfer) -->
          <div v-if="newTransactionType === 'Adding' || newTransactionType === 'Transfer'">
            <label class="block text-sm font-medium text-gray-700 mb-1">To Account</label>
            <select
              v-model="newTransactionToAccount"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">Select account</option>
              <option v-for="account in accounts" :key="account.id" :value="account.id">
                {{ account.name }} ({{ account.balance }} {{ account.currency }})
              </option>
            </select>
          </div>

          <!-- Category (for Debit and Adding) -->
          <div v-if="newTransactionType === 'Debit' || newTransactionType === 'Adding'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              v-model="newTransactionCategory"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
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
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <input
              v-model="newTransactionDescription"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter description"
            />
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showNewTransactionModal = false"
            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            @click="createNewTransaction"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Create Transaction
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dropdown-menu {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
</style>
