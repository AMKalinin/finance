<script setup>
import { ref, computed, watch } from 'vue'
import { friendApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const props = defineProps({
  modelValue: Boolean,
  editData: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref({
  friendId: '',
})

const errors = ref({})
const isLoading = ref(false)

// Доступные цвета аватаров
const availableAvatarColors = [
  'bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500',
  'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500',
  'bg-orange-500', 'bg-cyan-500', 'bg-amber-500', 'bg-emerald-500'
]

const avatarColor = ref('bg-blue-500')

const previewInitials = computed(() => {
  if (!form.value.friendId) return '??'
  return form.value.friendId.substring(0, 2).toUpperCase()
})

function validate() {
  errors.value = {}

  if (!form.value.friendId.trim()) {
    errors.value.friendId = 'ID пользователя обязателен'
  } else if (!/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(form.value.friendId)) {
    errors.value.friendId = 'Введите корректный UUID'
  }

  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return

  isLoading.value = true

  try {
    if (props.editData) {
      // Обновление статуса (принять/отклонить/отменить)
      if (props.editData.status === 'pending_received') {
        await friendApi.acceptRequest(props.editData.id)
      } else if (props.editData.status === 'pending_sent') {
        await friendApi.cancelSentRequest(props.editData.id)
      } else {
        await friendApi.declineRequest(props.editData.id)
      }
    } else {
      // Отправка запроса в дружбу
      await friendApi.create(form.value.friendId)
    }

    emit('saved')
    closeModal()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    errors.value.general = error.response?.data?.detail || 'Произошла ошибка при сохранении'
  } finally {
    isLoading.value = false
  }
}

function closeModal() {
  emit('update:modelValue', false)
  form.value = { friendId: '' }
  errors.value = {}
  avatarColor.value = 'bg-blue-500'
}

function loadEditData() {
  if (props.editData) {
    // Для редактирования используем ID как friendId
    form.value.friendId = props.editData.id
  }
}

const title = computed(() => {
  if (!props.editData) return 'Добавить друга'
  if (props.editData.status === 'pending_received') return 'Подтвердить дружбу'
  return 'Отменить запрос'
})

const submitLabel = computed(() => {
  if (isLoading.value) return 'Сохранение...'
  if (!props.editData) return t('actions.addFriend') || 'Добавить'
  if (props.editData.status === 'pending_received') return 'Принять'
  return 'Отменить'
})

const submitClass = computed(() => {
  if (isLoading.value) return 'bg-blue-400 cursor-not-allowed'
  if (!props.editData) return 'bg-blue-600 hover:bg-blue-700'
  if (props.editData.status === 'pending_received') return 'bg-green-600 hover:bg-green-700'
  return 'bg-red-600 hover:bg-red-700'
})

watch(() => props.modelValue, (val) => {
  if (val) {
    loadEditData()
  }
})
</script>

<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-md w-full border border-gray-200 dark:border-gray-700 overflow-hidden animate-fade-in">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ title }}</h3>
        <button @click="closeModal" class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-red-500 hover:text-white flex items-center justify-center transition-colors text-gray-600 dark:text-gray-400">✕</button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="px-6 py-4 space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
        <!-- General Error -->
        <div v-if="errors.general" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-3 rounded-lg text-sm text-red-700 dark:text-red-400">
          {{ errors.general }}
        </div>

        <!-- Friend ID -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            ID пользователя (UUID) *
          </label>
          <input
            v-model="form.friendId"
            type="text"
            :class="[
              'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all font-mono text-sm',
              errors.friendId
                ? 'border-red-500 bg-red-50 dark:bg-red-900/30'
                : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100'
            ]"
            placeholder="550e8400-e29b-41d4-a716-446655440000"
            :disabled="isLoading"
          />
          <p v-if="errors.friendId" class="mt-1 text-sm text-red-500">{{ errors.friendId }}</p>
          <p v-else class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Введите UUID пользователя, которого хотите добавить в друзья
          </p>
        </div>

        <!-- Avatar Color Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Цвет аватара
          </label>
          <div class="grid grid-cols-6 gap-2 max-h-40 overflow-y-auto p-2 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <button
              v-for="(color, index) in availableAvatarColors"
              :key="index"
              @click="avatarColor = color"
              type="button"
              class="w-full aspect-square flex items-center justify-center rounded hover:ring-2 ring-offset-2 dark:ring-offset-gray-900 transition-all"
              :class="{ 'ring-2 ring-blue-500': avatarColor === color, [color]: true }"
            >
              <span v-if="avatarColor === color" class="text-white text-lg">✓</span>
            </button>
          </div>
        </div>

        <!-- Preview -->
        <div class="flex items-center gap-4 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
          <div :class="[avatarColor, 'w-16 h-16 rounded-full flex items-center justify-center font-bold text-white text-xl']">
            {{ previewInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="font-medium text-gray-900 dark:text-gray-100 truncate">
              {{ form.friendId ? 'ID: ' + form.friendId : 'Предпросмотр' }}
            </h4>
            <p class="text-sm text-gray-500 dark:text-gray-400">UUID пользователя</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            type="submit"
            :disabled="isLoading"
            :class="['flex-1 px-4 py-2 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2', submitClass]"
          >
            <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!editData" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              <path v-else-if="editData.status === 'pending_received'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            {{ submitLabel }}
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
