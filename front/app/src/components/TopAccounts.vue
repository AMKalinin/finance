<script setup lang="ts">
  import { ref } from 'vue'
  import { EllipsisHorizontalIcon, PlusIcon } from '@heroicons/vue/24/outline'

  const emit = defineEmits(['addAccount', 'deleteAccount'])

  const props = defineProps<{
    accounts: any[]
  }>()

  const showNewAccountModal = ref(false)
  const showDropdown = ref<number | null>(null)
  const newAccountName = ref('')
  const newAccountBalance = ref('')
  const newAccountCurrency = ref('USD')

  const currencies = [
    { code: 'USD', name: 'US Dollar' },
    { code: 'EUR', name: 'Euro' },
    { code: 'GBP', name: 'British Pound' },
    { code: 'JPY', name: 'Japanese Yen' },
    { code: 'BTC', name: 'Bitcoin' },
    { code: 'ETH', name: 'Ethereum' },
    { code: 'LTC', name: 'Litecoin' },
  ]

  const toggleDropdown = (accountId: number) => {
    showDropdown.value = showDropdown.value === accountId ? null : accountId
  }

  const handleClickOutside = (event: Event) => {
    const target = event.target as HTMLElement
    if (!target.closest('.dropdown-menu') && !target.closest('.dropdown-trigger')) {
      showDropdown.value = null
    }
  }

  const openNewAccountModal = () => {
    showNewAccountModal.value = true
    newAccountName.value = ''
    newAccountBalance.value = ''
    newAccountCurrency.value = 'USD'
  }

  const createNewAccount = () => {
    if (newAccountName.value && newAccountBalance.value) {
      const balance = parseFloat(newAccountBalance.value)

      emit('addAccount', {
        id: props.accounts.length + 1,
        name: newAccountName.value,
        balance,
        change: '+0.0%',
        currency: newAccountCurrency.value
      })
      showNewAccountModal.value = false
    }
  }

  const deleteAccount = (accountId: number) => {
    // accounts.value = accounts.value.filter(account => account.id !== accountId)
    emit('deleteAccount', accountId)
    showDropdown.value = null
  }
</script>

<template>
  <div class="bg-white rounded-xl p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold">Accounts</h2>
      <button
        @click="openNewAccountModal"
        class="flex items-center gap-2 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
      >
        <PlusIcon class="w-5 h-5" />
        <span>Account</span>
      </button>
    </div>
    <div class="space-y-4">
      <div
        v-for="account in accounts"
        :key="account.id"
        class="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg relative"
      >
        <div>
          <div class="font-medium">{{ account.name }}</div>
          <div class="text-sm text-gray-500">{{ account.balance.toLocaleString() }} {{ account.currency }}</div>
        </div>
        <div class="flex items-center gap-3">
          <!-- <div :class="[ -->
          <!--   'text-sm', -->
          <!--   account.change.startsWith('+') ? 'text-green-600' : 'text-red-600' -->
          <!-- ]"> -->
          <!--   {{ account.change }} -->
          <!-- </div> -->
          <button
            class="dropdown-trigger p-1 hover:bg-gray-100 rounded-full"
            @click="toggleDropdown(account.id)"
          >
            <EllipsisHorizontalIcon class="w-5 h-5 text-gray-500" />
          </button>
          <div
            v-if="showDropdown === account.id"
            class="dropdown-menu absolute right-0 top-12 bg-white shadow-lg rounded-lg py-1 min-w-[120px] z-10"
          >
            <button
              class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
              @click="() => {}"
            >
              Edit
            </button>
            <button
              class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm text-red-600"
              @click="deleteAccount(account.id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- New Account Modal -->
    <div v-if="showNewAccountModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Create New Account</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Account Name</label>
            <input
              v-model="newAccountName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter account name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Currency</label>
            <select
              v-model="newAccountCurrency"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option v-for="currency in currencies" :key="currency.code" :value="currency.code">
                {{ currency.name }} ({{ currency.code }})
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Initial Balance</label>
            <input
              v-model="newAccountBalance"
              type="number"
              step="0.01"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter initial balance"
            />
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showNewAccountModal = false"
            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            @click="createNewAccount"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Create Account
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
