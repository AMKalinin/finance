<script setup lang="ts">
  import { ref } from 'vue'
  import { PlusIcon } from '@heroicons/vue/24/outline'

  const emit = defineEmits([
        'addTransaction', 'deleteTransaction'
        ])

  const props = defineProps<{
    transactions: any[]
  }>()

  const showNewTransactionModal = ref(false)
  const newTransactionType = ref('sent')
  const newTransactionAmount = ref('')
  const newTransactionSymbol = ref('BTC')
  const newTransactionTo = ref('')
  const newTransactionFrom = ref('')

  const openNewTransactionModal = () => {
    showNewTransactionModal.value = true
    newTransactionType.value = 'sent'
    newTransactionAmount.value = ''
    newTransactionSymbol.value = 'BTC'
    newTransactionTo.value = ''
    newTransactionFrom.value = ''
  }

  const createNewTransaction = () => {
    if (newTransactionAmount.value) {
      const newTransaction: any = {
        type: newTransactionType.value,
        amount: parseFloat(newTransactionAmount.value),
        symbol: newTransactionSymbol.value,
        date: new Date().toISOString().split('T')[0]
      }

      if (newTransactionType.value === 'sent' || newTransactionType.value === 'transfer') {
        newTransaction.to = newTransactionTo.value
      }

      if (newTransactionType.value === 'received' || newTransactionType.value === 'transfer') {
        newTransaction.from = newTransactionFrom.value
      }
      emit('addTransaction', newTransaction)
      // transactions.unshift(newTransaction)
      showNewTransactionModal.value = false
    }
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
                <div class="font-medium">
                  {{ tx.typeName === 'Debit' ? 'Sent' : tx.typeName === 'Adding' ? 'Received' : 'Transfer' }}
                </div>
                <!-- <div class="text-sm text-gray-500">{{ tx.symbol }}</div> -->
              </div>
            </div>
          </td>
          <td>{{ tx.size }} <!-- {{ tx.symbol }} --></td>
          <td class="font-mono text-sm">
            <template v-if="tx.typeName === 'Transfer'">
              {{ tx.FROM }} → {{ tx.TO }}
            </template>
            <template v-else>
              {{ tx.typeName === 'Debit' ? (tx.FROM + ' → ' + tx.category): (tx.category + ' → ' + tx.TO)}}
            </template>
          </td>
          <td>{{ new Date(tx.date).toLocaleDateString('ru-RU', {year: 'numeric', month: 'long', day: 'numeric'}) }}</td>
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
              <option value="sent">Sent</option>
              <option value="received">Received</option>
              <option value="transfer">Transfer</option>
            </select>
          </div>
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
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Currency</label>
            <select
              v-model="newTransactionSymbol"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="BTC">Bitcoin (BTC)</option>
              <option value="ETH">Ethereum (ETH)</option>
              <option value="LTC">Litecoin (LTC)</option>
              <option value="USD">US Dollar (USD)</option>
              <option value="EUR">Euro (EUR)</option>
            </select>
          </div>
          <div v-if="newTransactionType === 'sent' || newTransactionType === 'transfer'">
            <label class="block text-sm font-medium text-gray-700 mb-1">To</label>
            <input
              v-model="newTransactionTo"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter recipient address"
            />
          </div>
          <div v-if="newTransactionType === 'received' || newTransactionType === 'transfer'">
            <label class="block text-sm font-medium text-gray-700 mb-1">From</label>
            <input
              v-model="newTransactionFrom"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter sender address"
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
