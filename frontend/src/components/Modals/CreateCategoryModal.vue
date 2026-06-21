<script setup>
import { ref, computed, watch } from 'vue'
import { categoryApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const props = defineProps({
  modelValue: Boolean,
  editData: Object
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref({
  name: '',
  type: 'expense',
  parentId: null,
  icon: '📁'
})

const errors = ref({})
const isLoading = ref(false)
const parentCategories = ref([])
const loadingParents = ref(false)

function validate() {
  errors.value = {}

  if (!form.value.name.trim()) {
    errors.value.name = 'Название обязательно'
  }

  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return

  isLoading.value = true

  try {
    if (props.editData) {
      // Обновление имени: PUT /category/{id}/name
      await categoryApi.updateName(props.editData.id, form.value.name)
    } else {
      // Создание: POST /category/create
      const data = {
        name: form.value.name,
        type: form.value.type,
        parentCategory: form.value.parentId,
        level: form.value.parentId ? 2 : 1,
      }
      await categoryApi.create(data)
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
    type: 'expense',
    parentId: null,
    icon: '📁'
  }
  errors.value = {}
  parentCategories.value = []
}

function loadEditData() {
  if (props.editData) {
    form.value = { name: props.editData.name, type: props.editData.type, parentId: null, icon: '📁' }
  }
}

const title = computed(() => props.editData ? 'Редактировать категорию' : 'Новая категория')

// Загрузка категорий-родителей для выбранного типа
async function loadParentCategories() {
  loadingParents.value = true
  try {
    let response
    if (form.value.type === 'expense') {
      response = await categoryApi.getExpenses()
    } else if (form.value.type === 'income') {
      response = await categoryApi.getIncome()
    } else {
      response = await categoryApi.getAll()
    }
    // Бэкенд возвращает { items: [root categories with subCategory] }
    const allItems = response.data?.items || []
    // Собираем все категории (корневые + вложенные) для выбранного типа
    const flat = []
    for (const cat of allItems) {
      flat.push(cat)
      const subs = cat.subCategory || cat.children || []
      for (const child of subs) {
        flat.push(child)
        // Рекурсивно собираем grandchildren
        const gsubs = child.subCategory || child.children || []
        for (const gc of gsubs) {
          flat.push(gc)
        }
      }
    }
    // Фильтруем: только категории текущего типа, исключаем саму категорию при редактировании
    const currentType = form.value.type
    parentCategories.value = flat.filter(c => c.type === currentType && (!props.editData || c.id !== props.editData.id))
  } catch (error) {
    console.error('Ошибка загрузки родителей:', error)
    parentCategories.value = []
  } finally {
    loadingParents.value = false
  }
}

// Фильтрация родителей по типу при изменении
async function onTypeChange() {
  parentCategories.value = []
  form.value.parentId = null
  await loadParentCategories()
}

function onOpen() {
  if (props.modelValue) {
    loadEditData()
    loadParentCategories()
  }
}

watch(() => props.modelValue, (val) => {
  if (val) onOpen()
})

watch(() => form.value.type, () => {
  onTypeChange()
})

// Доступные иконки для выбора
const availableIcons = [
  '📁', '🏠', '💼', '🛒', '☕', '🚗', '⛽', '🎮', '🎬',
  '🎭', '🎸', '💊', '🏥', '📚', '✈️', '🏨', '👔', '👗',
  '🧴', '🛍️', '🎁', '🕯️', '🌱', '🐕', '🐱'
]

function setIcon(icon) {
  form.value.icon = icon
}

// Получить отступ для визуального отображения иерархии
function getCategoryIndent(cat) {
  const level = cat.level || 1
  const indent = '  '.repeat(level - 1)
  return indent + (level > 1 ? '└─ ' : '')
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
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            :class="{ 'border-red-500 bg-red-50 dark:bg-red-900/20': errors.name }"
            placeholder="Например: Супермаркеты"
          />
          <p v-if="errors.name" class="mt-1 text-sm text-red-500">{{ errors.name }}</p>
        </div>

        <!-- Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Тип категории</label>
          <select v-model="form.type" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
            <option value="expense">Расходы</option>
            <option value="income">Доходы</option>
            <option value="transfer">Переводы</option>
          </select>
        </div>

        <!-- Icon Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Иконка категории</label>
          <div class="grid grid-cols-8 gap-2 max-h-48 overflow-y-auto p-1 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <button
              v-for="icon in availableIcons"
              :key="icon"
              @click="setIcon(icon)"
              type="button"
              class="w-full aspect-square flex items-center justify-center text-xl rounded hover:bg-white dark:hover:bg-gray-800 transition-colors"
              :class="{ 'bg-blue-100 dark:bg-blue-900/30 ring-2 ring-blue-500': form.icon === icon }"
            >
              {{ icon }}
            </button>
          </div>
        </div>

        <!-- Parent Category -->
        <div v-if="form.type !== 'transfer'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Родительская категория</label>
          <select
            v-model="form.parentId"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          >
            <option :value="null">Без родителя (корневая категория)</option>
            <template v-if="loadingParents">
              <option disabled>Загрузка...</option>
            </template>
            <template v-else>
              <option v-for="parent in parentCategories" :key="parent.id" :value="parent.id">
                {{ getCategoryIndent(parent) }}{{ parent.icon || '📁' }} {{ parent.name }}
              </option>
            </template>
            <option v-if="!loadingParents && parentCategories.length === 0" disabled value="">Нет доступных категорий</option>
          </select>
          <p v-if="!loadingParents && parentCategories.length === 0" class="mt-1 text-xs text-gray-500 dark:text-gray-400">Сначала создайте корневую категорию этого типа</p>
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
