<script setup>
import { ref, computed } from 'vue'
import { accountApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const props = defineProps({
  modelValue: Boolean,
  editData: Object
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref({
  name: '',
  type: 'debit',
  currency: 'RUB',
  balance: 0,
  interestRate: 0,
  isPrimary: false,
  description: ''
})

const errors = ref({})
const isLoading = ref(false)

function validate() {
  errors.value = {}

  if (!form.value.name.trim()) {
    errors.value.name = 'Название обязательно'
  }

  if (form.value.balance < 0) {
    errors.value.balance = t('accountForm.savings') + ' не может быть отрицательным'
  }

  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return

  isLoading.value = true

  try {
    if (props.editData) {
      // Обновление полей — бэкенд требует отдельные endpoint'ы
      await accountApi.updateName(props.editData.id, form.value.name)
      await accountApi.updateDescription(props.editData.id, form.value.description)
      await accountApi.updateInterestRate(props.editData.id, form.value.interestRate)
      await accountApi.updatePrimary(props.editData.id, form.value.isPrimary)
    } else {
      // Создание нового счета — snake_case для бэкенда
      const data = accountApi.mapToBackend({
        name: form.value.name,
        type: form.value.type,
        currency: form.value.currency,
        balance: form.value.balance,
        interestRate: form.value.interestRate,
        isPrimary: form.value.isPrimary,
        description: form.value.description,
      })
      await accountApi.create(data)
    }

    emit('saved')
    closeModal()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    errors.value.general = 'Произошла ошибка при сохранении'
  } finally {
    isLoading.value = false
  }
}

function closeModal() {
  emit('update:modelValue', false)
  form.value = {
    name: '',
    type: 'debit',
    currency: 'RUB',
    balance: 0,
    interestRate: 0,
    isPrimary: false,
    description: ''
  }
  errors.value = {}
}

// Заполняем форму при редактировании
function loadEditData() {
  if (props.editData) {
    form.value = { ...props.editData }
  }
}

const title = computed(() => props.editData ? 'Редактировать счет' : 'Новый счёт')

// Загружаем данные при открытии модалки
function onOpen() {
  if (props.modelValue) {
    loadEditData()
  }
}
</script>

<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-md w-full border border-gray-200 dark:border-gray-700 overflow-hidden animate-fade-in">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ title }}</h3>
        <button @click="closeModal" class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-red-500 hover:text-white flex items-center justify-center transition-colors">✕</button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="px-6 py-4 space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
        <!-- General Error -->
        <div v-if="errors.general" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-3 rounded-lg text-sm text-red-700 dark:text-red-400">
          {{ errors.general }}
        </div>

        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('accountForm.accountName') }} *</label>
          <input
            v-model="form.name"
            type="text"
            :class="[
              'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
              errors.name ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            ]"
            placeholder="Например: Основной банковский"
          />
          <p v-if="errors.name" class="mt-1 text-sm text-red-500">{{ errors.name }}</p>
        </div>

        <!-- Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('accountForm.accountType') }}</label>
          <select v-model="form.type" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
            <option value="debit">Дебетовая карта</option>
            <option value="credit">Кредитная карта</option>
            <option value="cash">Наличные</option>
            <option value="investment">Инвестиционный</option>
            <option value="savings">Сберегательный счет</option>
          </select>
        </div>

        <!-- Currency -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('accountForm.currency') }}</label>
          <select v-model="form.currency" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
            <option value="RUB">RUB - Рубли</option>
            <option value="USD">USD - Доллары</option>
            <option value="EUR">EUR - Евро</option>
          </select>
        </div>

        <!-- Balance -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('common.balance') }}</label>
          <input
            v-model.number="form.balance"
            type="number"
            step="0.01"
            :class="[
              'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
              errors.balance ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            ]"
          />
          <p v-if="errors.balance" class="mt-1 text-sm text-red-500">{{ errors.balance }}</p>
        </div>

        <!-- Interest Rate -->
        <div v-if="form.type === 'savings' || form.type === 'investment'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('accountForm.interestRate') }}</label>
          <input
            v-model.number="form.interestRate"
            type="number"
            step="0.1"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>

        <!-- Primary Account -->
        <div class="flex items-center gap-2">
          <input
            v-model="form.isPrimary"
            type="checkbox"
            id="isPrimary"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer"
          />
          <label for="isPrimary" class="text-sm text-gray-700 dark:text-gray-300 cursor-pointer select-none">{{ t('common.primaryAccount') }}</label>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ t('accountForm.description') }} {{ t('common.optionalField') }}</label>
          <textarea
            v-model="form.description"
            rows="2"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
            placeholder="Дополнительная информация о счете..."
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            type="submit"
            :disabled="isLoading"
            class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
            </svg>
            {{ isLoading ? t('common.saving') : (editData ? t('common.update') : t('common.create')) }}
          </button>
          <button
            type="button"
            @click="closeModal"
            class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors"
          >
            {{ t('common.cancel') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
