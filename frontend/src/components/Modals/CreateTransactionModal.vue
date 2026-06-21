<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { transactionApi } from '@/api/client'
import { accountApi } from '@/api/client'
import { categoryApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'
import { isUserAuthenticated } from '@/keycloak/keycloak-init'

const { t } = useLanguageStore()

const props = defineProps({
  modelValue: Boolean,
  editData: Object
})

const emit = defineEmits(['update:modelValue', 'saved'])

const activeTab = ref('general') // 'general' | 'positions'

const form = ref({
  type: 'debit',
  fromAccountId: null,
  toAccountId: null,
  categoryId: null,
  amount: '',
  currency: 'RUB',
  date: new Date().toISOString().split('T')[0],
  description: ''
})

const errors = ref({})
const isLoading = ref(false)

// Данные для форм
const accounts = ref([])
const categories = ref([])
const loadingAccounts = ref(false)
const loadingCategories = ref(false)
const errorAccounts = ref(null)
const errorCategories = ref(null)

// Позиции
const positions = ref([])
const editingPositionIndex = ref(-1)

function resetPositions() {
  positions.value = []
  editingPositionIndex.value = -1
}

function addPosition() {
  editingPositionIndex.value = positions.value.length
  positions.value.push({
    name: '',
    price: '',
    quantity: ''
  })
}

function removePosition(index) {
  positions.value.splice(index, 1)
  if (editingPositionIndex.value === index) {
    editingPositionIndex.value = -1
  } else if (editingPositionIndex.value > index) {
    editingPositionIndex.value--
  }
}

function savePosition(index, field, value) {
  if (positions.value[index]) {
    positions.value[index][field] = value
  }
}

function cancelEditPosition() {
  editingPositionIndex.value = -1
}

function validatePositions() {
  const positionErrors = []
  positions.value.forEach((pos, index) => {
    const errs = []
    if (!pos.name?.trim()) errs.push('Название')
    const price = parseFloat(pos.price)
    if (!pos.price || isNaN(price) || price <= 0) errs.push('Цена')
    const quantity = parseFloat(pos.quantity)
    if (!pos.quantity || isNaN(quantity) || quantity <= 0) errs.push('Количество')
    if (errs.length > 0) {
      positionErrors.push(`Позиция ${index + 1}: ${errs.join(', ')}`)
    }
  })
  return positionErrors
}

function validate() {
  errors.value = {}

  const amountVal = parseFloat(form.value.amount)
  if (!form.value.amount || isNaN(amountVal) || amountVal <= 0) {
    errors.value.amount = 'Введите корректную сумму'
  }

  if (form.value.type === 'debit' && !form.value.fromAccountId) {
    errors.value.fromAccount = 'Выберите счет списания'
  }

  if (form.value.type === 'adding' && !form.value.toAccountId) {
    errors.value.toAccount = 'Выберите счет зачисления'
  }

  if (form.value.type === 'transfer' && (!form.value.fromAccountId || !form.value.toAccountId)) {
    errors.value.fromAccount = 'Выберите счета'
  }

  // Категория обязательна только для debit и adding, не для transfer
  if (form.value.categoryId === null || form.value.categoryId === undefined || form.value.categoryId === '') {
    if (form.value.type !== 'transfer') {
      errors.value.category = 'Выберите категорию'
    }
  }

  // Валидация позиций
  const positionErrors = validatePositions()
  if (positionErrors.length > 0) {
    errors.value.positions = positionErrors
  }

  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return

  isLoading.value = true

  try {
    const amount = parseFloat(form.value.amount)
    let backendData = {
      type: form.value.type,
      date: form.value.date,
      description: form.value.description || '',
      status: 'settled'
    }

    if (form.value.type === 'debit') {
      backendData = {
        ...backendData,
        FROM: form.value.fromAccountId,
        category: form.value.categoryId,
        debitSize: amount,
        creditSize: null
      }
    } else if (form.value.type === 'adding') {
      backendData = {
        ...backendData,
        TO: form.value.toAccountId,
        category: form.value.categoryId,
        debitSize: 0,
        creditSize: amount
      }
    } else if (form.value.type === 'transfer') {
      backendData = {
        ...backendData,
        FROM: form.value.fromAccountId,
        TO: form.value.toAccountId,
        category: null,
        debitSize: amount,
        creditSize: amount
      }
    }

    // Бэкенд ожидает плоскую структуру, НЕ обёрнутую в transaction_info
    const payload = {
      ...backendData
    }

    // Добавляем позиции на верхний уровень
    if (positions.value.length > 0) {
      payload.positions = positions.value.map(pos => ({
        name: pos.name.trim(),
        price: parseFloat(pos.price),
        quantity: parseFloat(pos.quantity)
      }))
    }

    if (props.editData) {
      await transactionApi.update(props.editData.id, payload)
    } else {
      await transactionApi.create(payload)
    }

    emit('saved')
    closeModal()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    errors.value.general = 'Произошла ошибка при сохранении: ' + (error.message || 'неизвестная ошибка')
  } finally {
    isLoading.value = false
  }
}

function closeModal() {
  emit('update:modelValue', false)
  form.value = {
    type: 'debit',
    fromAccountId: null,
    toAccountId: null,
    categoryId: null,
    amount: '',
    currency: 'RUB',
    date: new Date().toISOString().split('T')[0],
    description: ''
  }
  errors.value = {}
  resetPositions()
  activeTab.value = 'general'
}

function loadEditData() {
  if (props.editData) {
    form.value = {
      type: props.editData.type || 'debit',
      fromAccountId: props.editData.fromAccountId || null,
      toAccountId: props.editData.toAccountId || null,
      categoryId: props.editData.categoryId || props.editData.category?.id || null,
      amount: props.editData.amount ? Math.abs(props.editData.amount).toString() : '',
      currency: props.editData.currency || 'RUB',
      date: props.editData.date || new Date().toISOString().split('T')[0],
      description: props.editData.description || ''
    }
    // Загружаем позиции
    if (props.editData.positions && props.editData.positions.length > 0) {
      positions.value = props.editData.positions.map(p => ({
        name: p.name || '',
        price: p.price?.toString() || '',
        quantity: p.quantity?.toString() || ''
      }))
    } else {
      resetPositions()
    }
  } else {
    resetPositions()
  }
}

const title = computed(() => props.editData ? 'Редактировать транзакцию' : 'Новая транзакция')

// Загрузка счетов
async function loadAccounts() {
  loadingAccounts.value = true
  errorAccounts.value = null
  accounts.value = []
  // Проверка аутентификации
  if (!isUserAuthenticated()) {
    errorAccounts.value = 'Необходимо войти в систему'
    loadingAccounts.value = false
    return
  }
  try {
    const response = await accountApi.getAll()
    const data = response.data || {}
    // Обработка разных форматов ответа от API
    const items = (data.items || data || [])

    accounts.value = items.map(acc => ({
      id: acc.id,
      name: acc.name,
      type: acc.type || acc.account_type,
      currency: acc.currency,
      balance: acc.balance
    }))
    errorAccounts.value = null
  } catch (error) {
    console.error('Ошибка загрузки счетов:', error)
    errorAccounts.value = error.message || 'Не удалось загрузить счета'
    accounts.value = []
  } finally {
    loadingAccounts.value = false
  }
}

// Загрузка категорий
async function loadCategories() {
  loadingCategories.value = true
  errorCategories.value = null
  categories.value = []
  // Проверка аутентификации
  if (!isUserAuthenticated()) {
    errorCategories.value = 'Необходимо войти в систему'
    loadingCategories.value = false
    return
  }
  try {
    const response = await categoryApi.getAll()
    const data = response.data || {}
    // Обработка разных форматов ответа от API
    const items = (data.items || data || [])

    // Собираем все категории (корневые + вложенные)
    const allCats = []
    for (const cat of items) {
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
    categories.value = allCats.map(cat => ({
      id: cat.id,
      name: cat.name,
      type: cat.type,
      icon: cat.icon
    }))
    errorCategories.value = null
  } catch (error) {
    console.error('Ошибка загрузки категорий:', error)
    errorCategories.value = error.message || 'Не удалось загрузить категории'
    categories.value = []
  } finally {
    loadingCategories.value = false
  }
}

// Фильтрация категорий по типу
const filteredCategories = computed(() => {
  if (!categories.value.length) return []
  if (form.value.type === 'debit') {
    return categories.value.filter(c => c.type === 'expense')
  } else if (form.value.type === 'adding') {
    return categories.value.filter(c => c.type === 'income')
  }
  return categories.value
})

// Получение названия счета
function getAccountName(id) {
  const acc = accounts.value.find(a => a.id === id)
  return acc ? acc.name : 'Неизвестно'
}

// Получение иконки категории
function getCategoryIcon(cat) {
  return cat?.icon || '📁'
}

function onOpen() {
  if (props.modelValue) {
    loadEditData()
    // Данные уже загружены в onMounted, но обновляем их при редактировании
    loadAccounts()
    loadCategories()
  }
}

watch(() => props.modelValue, (val) => {
  if (val) onOpen()
})

// При смене типа очищаем categoryId если он не подходит
watch(() => form.value.type, () => {
  form.value.categoryId = null
})

// Доступные иконки для выбора
// Загрузка счетов и категорий при создании компонента
onMounted(() => {
  loadAccounts()
  loadCategories()
})

const availableIcons = [
  '📁', '🏠', '💼', '🛒', '☕', '🚗', '⛽', '🎮', '🎬',
  '🎭', '🎸', '💊', '🏥', '📚', '✈️', '🏨', '👔', '👗',
  '🧴', '🛍️', '🎁', '🕯️', '🌱', '🐕', '🐱'
]

function formatAmount(value) {
  return value ? parseFloat(value).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) : ''
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

      <!-- Tabs -->
      <div class="flex border-b border-gray-200 dark:border-gray-700 px-4">
        <button
          @click="activeTab = 'general'"
          class="px-4 py-3 text-sm font-medium transition-colors border-b-2"
          :class="activeTab === 'general'
            ? 'border-blue-600 text-blue-600 dark:text-blue-400'
            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
        >
          📋 Основная
        </button>
        <button
          @click="activeTab = 'positions'"
          class="px-4 py-3 text-sm font-medium transition-colors border-b-2 relative"
          :class="activeTab === 'positions'
            ? 'border-blue-600 text-blue-600 dark:text-blue-400'
            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
        >
          📊 Позиции
          <span v-if="positions.length > 0" class="absolute top-1 right-2 w-5 h-5 bg-blue-600 text-white text-xs rounded-full flex items-center justify-center">
            {{ positions.length }}
          </span>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="px-6 py-4 space-y-4 max-h-[calc(100vh-280px)] overflow-y-auto">
        <!-- General Error -->
        <div v-if="errors.general" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-3 rounded-lg text-sm text-red-700 dark:text-red-400">
          {{ errors.general }}
        </div>

        <!-- ==================== GENERAL TAB ==================== -->
        <div v-if="activeTab === 'general'" class="space-y-4">
          <!-- Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Тип транзакции</label>
            <select v-model="form.type" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all">
              <option value="debit">Расход</option>
              <option value="adding">Доход</option>
              <option value="transfer">Перевод</option>
            </select>
          </div>

          <!-- Amount -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Сумма *</label>
            <input
              v-model="form.amount"
              type="number"
              step="0.01"
              min="0"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
              :class="errors.amount ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
              placeholder="0.00"
            />
            <p v-if="errors.amount" class="mt-1 text-sm text-red-500">{{ errors.amount }}</p>
          </div>

          <!-- Currency -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Валюта</label>
            <select v-model="form.currency" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all">
              <option value="RUB">₽ RUB</option>
              <option value="USD">$ USD</option>
              <option value="EUR">€ EUR</option>
            </select>
          </div>

          <!-- Account Selection -->
          <template v-if="form.type === 'debit'">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Счет списания *</label>
              <select
                v-model="form.fromAccountId"
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
                :class="errors.fromAccount ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
              >
                <option value="">Выберите счет...</option>
                <option v-if="loadingAccounts" disabled>Загрузка...</option>
                <option v-else-if="!errorAccounts" v-for="acc in accounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
              </select>
              <p v-if="errors.fromAccount" class="mt-1 text-sm text-red-500">{{ errors.fromAccount }}</p>
              <p v-if="errorAccounts" class="mt-1 text-sm text-red-500">{{ errorAccounts }} <button @click="loadAccounts" class="underline">Повторить</button></p>
            </div>
          </template>

          <template v-if="form.type === 'adding'">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Счет зачисления *</label>
              <select
                v-model="form.toAccountId"
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
                :class="errors.toAccount ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
              >
                <option value="">Выберите счет...</option>
                <option v-if="loadingAccounts" disabled>Загрузка...</option>
                <option v-else-if="!errorAccounts" v-for="acc in accounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
              </select>
              <p v-if="errors.toAccount" class="mt-1 text-sm text-red-500">{{ errors.toAccount }}</p>
              <p v-if="errorAccounts" class="mt-1 text-sm text-red-500">{{ errorAccounts }} <button @click="loadAccounts" class="underline">Повторить</button></p>
            </div>
          </template>

          <!-- Transfer: both accounts -->
          <template v-if="form.type === 'transfer'">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Счет списания *</label>
              <select
                v-model="form.fromAccountId"
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
                :class="errors.fromAccount ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
              >
                <option value="">Выберите счет...</option>
                <option v-if="loadingAccounts" disabled>Загрузка...</option>
                <option v-else-if="!errorAccounts" v-for="acc in accounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
              </select>
              <p v-if="errorAccounts" class="mt-1 text-sm text-red-500">{{ errorAccounts }} <button @click="loadAccounts" class="underline">Повторить</button></p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Счет зачисления *</label>
              <select
                v-model="form.toAccountId"
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
                :class="errors.toAccount ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
              >
                <option value="">Выберите счет...</option>
                <option v-if="loadingAccounts" disabled>Загрузка...</option>
                <option v-else-if="!errorAccounts" v-for="acc in accounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
              </select>
              <p v-if="errorAccounts" class="mt-1 text-sm text-red-500">{{ errorAccounts }} <button @click="loadAccounts" class="underline">Повторить</button></p>
            </div>
          </template>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Категория *</label>
            <select
              v-model="form.categoryId"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
              :class="errors.category ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'"
            >
              <option v-if="loadingCategories" disabled>Загрузка...</option>
              <option v-else-if="!errorCategories" v-for="cat in filteredCategories" :key="cat.id" :value="cat.id">
                {{ getCategoryIcon(cat) }} {{ cat.name }}
              </option>
              <option v-else disabled>Ошибка загрузки</option>
            </select>
            <p v-if="errorCategories" class="mt-1 text-sm text-red-500">{{ errorCategories }} <button @click="loadCategories" class="underline">Повторить</button></p>
            <p v-if="errors.category && !errorCategories" class="mt-1 text-sm text-red-500">{{ errors.category }}</p>
          </div>

          <!-- Date -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Дата</label>
            <input
              v-model="form.date"
              type="date"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Описание (необязательно)</label>
            <textarea
              v-model="form.description"
              rows="2"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all resize-none"
              placeholder="Дополнительная информация..."
            ></textarea>
          </div>
        </div>

        <!-- ==================== POSITIONS TAB ==================== -->
        <div v-if="activeTab === 'positions'" class="space-y-3">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Добавьте позиции (акции, облигации, криптовалюты и т.д.), связанные с этой транзакцией.
          </p>

          <!-- Position errors -->
          <div v-if="errors.positions" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-3 rounded-lg text-sm text-red-700 dark:text-red-400">
            <p class="font-medium mb-1">Ошибка в позициях:</p>
            <ul class="list-disc list-inside">
              <li v-for="(err, i) in errors.positions" :key="i">{{ err }}</li>
            </ul>
          </div>

          <!-- Positions list -->
          <div v-if="positions.length === 0" class="text-center py-8 text-gray-400 dark:text-gray-500">
            <p class="text-3xl mb-2">📊</p>
            <p>Нет позиций</p>
            <p class="text-sm">Нажмите кнопку ниже, чтобы добавить</p>
          </div>

          <div v-for="(pos, index) in positions" :key="index" class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3 bg-gray-50 dark:bg-gray-900/50">
            <!-- Position header -->
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Позиция {{ index + 1 }}</span>
              <button
                type="button"
                @click="removePosition(index)"
                class="text-red-500 hover:text-red-700 hover:bg-red-100 dark:hover:bg-red-900/30 p-1 rounded transition-colors"
                title="Удалить позицию"
              >
                🗑️
              </button>
            </div>

            <!-- Name -->
            <div>
              <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Название *</label>
              <input
                v-model="pos.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all text-sm"
                placeholder="AAPL, BTC, SBER..."
              />
            </div>

            <!-- Price and Quantity -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Цена *</label>
                <input
                  v-model="pos.price"
                  type="number"
                  step="0.01"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all text-sm"
                  placeholder="0.00"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Количество *</label>
                <input
                  v-model="pos.quantity"
                  type="number"
                  step="0.0001"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all text-sm"
                  placeholder="0.00"
                />
              </div>
            </div>

            <!-- Total -->
            <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pt-1 border-t border-gray-200 dark:border-gray-700">
              <span>Итого:</span>
              <span class="font-medium text-gray-700 dark:text-gray-300">
                {{ formatAmount((parseFloat(pos.price) || 0) * (parseFloat(pos.quantity) || 0)) }}
              </span>
            </div>
          </div>

          <!-- Add position button -->
          <button
            type="button"
            @click="addPosition"
            class="w-full py-2.5 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-gray-500 dark:text-gray-400 hover:border-blue-500 hover:text-blue-600 dark:hover:border-blue-400 dark:hover:text-blue-400 transition-colors flex items-center justify-center gap-2 text-sm font-medium"
          >
            ➕ Добавить позицию
          </button>
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
            {{ isLoading ? 'Сохранение...' : (props.editData ? 'Обновить' : 'Создать') }}
          </button>
          <button
            type="button"
            @click="closeModal"
            class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors"
          >
            Отмена
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
