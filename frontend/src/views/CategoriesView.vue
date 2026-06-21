<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import CategoryTree from '@/components/CategoryTree.vue'
import { categoryApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const categories = ref([])
const loading = ref(false)
const error = ref(null)
const currentFilter = ref('all') // all, expense, income, transfer

// Категории по типам для отображения
const expenseCategories = computed(() => {
  return categories.value.filter(c => c.type === 'expense')
})

const incomeCategories = computed(() => {
  return categories.value.filter(c => c.type === 'income')
})

const transferCategories = computed(() => {
  return categories.value.filter(c => c.type === 'transfer')
})

async function loadCategories() {
  loading.value = true
  error.value = null
  try {
    const response = await categoryApi.getAll()
    // Бэкенд возвращает: { items: [...], total, skip, limit, has_more }
    // items — это корневые категории (level=1) с вложенными children (subCategory)
    categories.value = response.data?.items || []
  } catch (err) {
    console.error('Ошибка загрузки категорий:', err)
    error.value = err.message || 'Не удалось загрузить категории'
  } finally {
    loading.value = false
  }
}

async function loadCategoriesByType(type) {
  loading.value = true
  error.value = null
  try {
    const endpoint = type === 'expense' ? 'getExpenses' : type === 'income' ? 'getIncome' : null
    if (endpoint) {
      const response = await categoryApi[endpoint]()
      categories.value = response.data?.items || []
    }
  } catch (err) {
    console.error(`Ошибка загрузки категорий (${type}):`, err)
    error.value = err.message || 'Не удалось загрузить категории'
  } finally {
    loading.value = false
  }
}

function filterCategories(type) {
  currentFilter.value = type
  if (type === 'all') {
    loadCategories()
  } else {
    loadCategoriesByType(type)
  }
}

function openEditCategory(category) {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'category', data: category } }))
}

function openNewCategoryModal() {
  window.dispatchEvent(new CustomEvent('openModal', { detail: { type: 'category' } }))
}

async function deleteCategory(id, name) {
  if (confirm(`Вы уверены, что хотите удалить категорию "${name}" и всех её потомков?`)) {
    try {
      await categoryApi.delete(id)
      // Перезагрузить данные
      loadCategories()
    } catch (err) {
      console.error('Ошибка удаления категории:', err)
      alert('Не удалось удалить категорию: ' + (err.message || 'неизвестная ошибка'))
    }
  }
}

function onModalSaved() {
  loadCategories()
}

// Фильтрация детей на клиенте по типу
function filterChildren(children) {
  if (!children) return []
  if (currentFilter.value === 'all') return children
  return children.filter(c => c.type === currentFilter.value)
}

onMounted(() => {
  loadCategories()
  window.addEventListener('modalSaved', handleModalSaved)
})

onUnmounted(() => {
  window.removeEventListener('modalSaved', handleModalSaved)
})

function handleModalSaved(event) {
  if (event.detail?.type === 'category') {
    loadCategories()
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">📁 Категории</h1>
      <button @click="openNewCategoryModal" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
        ➕ {{ t("actions.createCategory") }}
      </button>
    </div>

    <!-- Search -->
    <div class="relative">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input type="text" v-bind:placeholder="t('common.searchCategories')" class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-2">
      <button
        @click="filterCategories('all')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium cursor-pointer transition-colors',
          currentFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
        ]">
        {{ t('common.allTypes') }}
      </button>
      <button
        @click="filterCategories('expense')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium cursor-pointer transition-colors',
          currentFilter === 'expense' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
        ]">
        Расходы
      </button>
      <button
        @click="filterCategories('income')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium cursor-pointer transition-colors',
          currentFilter === 'income' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
        ]">
        Доходы
      </button>
      <button
        @click="filterCategories('transfer')"
        :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium cursor-pointer transition-colors',
          currentFilter === 'transfer' ? 'bg-blue-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
        ]">
        Переводы
      </button>
    </div>

    <!-- Loading / Error states -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="flex items-center gap-3 text-gray-500">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Загрузка категорий...</span>
      </div>
    </div>

    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-4 rounded-lg text-red-700 dark:text-red-400">
      <p class="font-medium">Ошибка загрузки</p>
      <p class="text-sm">{{ error }}</p>
      <button @click="loadCategories" class="mt-2 text-sm underline hover:no-underline">Попробовать снова</button>
    </div>

    <!-- Category Tree with Edit/Delete Actions -->
    <div v-if="!loading && !error" class="space-y-6">
      <!-- Expenses Tree -->
      <div v-if="currentFilter === 'all' || currentFilter === 'expense'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🔴 Расходы</h2>
        <CategoryTree
          v-if="expenseCategories.length"
          :categories="expenseCategories"
          :level="0"
          @edit="openEditCategory"
          @delete="deleteCategory"
        />
        <div v-else class="text-center py-4 text-gray-500 dark:text-gray-400">
          <p>Нет категорий расходов</p>
        </div>
      </div>

      <!-- Income Tree -->
      <div v-if="currentFilter === 'all' || currentFilter === 'income'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🟢 Доходы</h2>
        <CategoryTree
          v-if="incomeCategories.length"
          :categories="incomeCategories"
          :level="0"
          @edit="openEditCategory"
          @delete="deleteCategory"
        />
        <div v-else class="text-center py-4 text-gray-500 dark:text-gray-400">
          <p>Нет категорий доходов</p>
        </div>
      </div>

      <!-- Transfer Tree -->
      <div v-if="currentFilter === 'all' || currentFilter === 'transfer'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🔵 Переводы</h2>
        <CategoryTree
          v-if="transferCategories.length"
          :categories="transferCategories"
          :level="0"
          @edit="openEditCategory"
          @delete="deleteCategory"
        />
        <div v-else class="text-center py-4 text-gray-500 dark:text-gray-400">
          <p>Нет категорий переводов</p>
        </div>
      </div>

      <div v-if="categories.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <p>Нет категорий</p>
        <button @click="openNewCategoryModal" class="mt-2 text-blue-600 hover:underline text-sm">Создать первую категорию</button>
      </div>
    </div>

    <!-- Category Stats (Example) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">📊 Статистика категорий</h3>
        <div class="space-y-3">
          <div v-for="(category, index) in categories.slice(0, 5)" :key="index" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ category.name }}</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-gray-100">₽ {{ (Math.random() * 50000).toFixed(2) }}</span>
          </div>
          <div v-if="categories.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400 text-sm">
            Создайте категории для отображения статистики
          </div>
        </div>
      </div>

      <!-- Popular Categories -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 md:col-span-2">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🔥 Популярные категории</h3>
        <div class="flex flex-wrap gap-2">
          <span v-for="(category, index) in categories.slice(0, 8)" :key="index" class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-sm cursor-pointer transition-colors flex items-center gap-2">
            <span>{{ category.icon || '📁' }}</span>
            <span>{{ category.name }}</span>
          </span>
          <div v-if="categories.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400 text-sm w-full">
            Создайте категории для отображения
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom tree styling */
ul {
  list-style: none;
}
</style>
