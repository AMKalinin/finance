<script setup>
import { ref, computed, watch } from 'vue'
import { distributionApi, friendApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'

const { t } = useLanguageStore()

const props = defineProps({
  modelValue: Boolean,
  transactionId: { type: String, required: true },
  transactionAmount: { type: Number, required: true },
  transactionCurrency: { type: String, default: 'RUB' },
  existingDistributions: { type: Array, default: () => [] },
  isNewTransaction: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'saved'])

// Состояние
const isLoading = ref(false)
const error = ref('')

// Тип разделения
const splitType = ref('equal')

// Участники
const participants = ref([])

// Друзья для выбора
const friends = ref([])
const loadingFriends = ref(false)
const friendError = ref('')

// Поиск друзей
const searchQuery = ref('')

// Выбранный друг для добавления
const showFriendPicker = ref(false)

// Редактирование
const editingIndex = ref(-1)
const editingSize = ref('')

// Текущий пользователь (владелец)
const currentUser = ref(null)

// Вычисленные размеры для каждого участника
const computedSizes = computed(() => {
  if (splitType.value === 'equal') {
    const totalPeople = participants.value.length
    if (totalPeople === 0) return []
    const share = Math.round((props.transactionAmount / totalPeople) * 100) / 100
    return participants.value.map((p, i) => ({
      ...p,
      size: share,
      isOwner: p.isOwner
    }))
  }
  return participants.value.map(p => ({
    ...p,
    size: p.size || 0,
    isOwner: p.isOwner
  }))
})

// Общая сумма распределения
const totalDistributed = computed(() => {
  return computedSizes.value.reduce((sum, p) => sum + (p.size || 0), 0)
})

// Остаток
const remainder = computed(() => {
  return Math.round((props.transactionAmount - totalDistributed.value) * 100) / 100
})

// Фильтрованные друзья
const filteredFriends = computed(() => {
  if (!searchQuery.value) return friends.value
  const q = searchQuery.value.toLowerCase()
  return friends.value.filter(f =>
    f.name.toLowerCase().includes(q) || f.initials.toLowerCase().includes(q)
  )
})

// Аватар цвета
const avatarColors = [
  'bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500',
  'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500',
  'bg-orange-500', 'bg-cyan-500', 'bg-amber-500', 'bg-emerald-500'
]

function getRandomColor(seed) {
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  return avatarColors[Math.abs(hash) % avatarColors.length]
}

function getInitials(name) {
  if (!name) return '??'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

// Загрузка друзей
async function loadFriends() {
  loadingFriends.value = true
  friendError.value = ''
  try {
    const res = await friendApi.getAll()
    const data = res.data?.items || res.data?.friends || res.data || []
    friends.value = data.map(f => ({
      id: f.id,
      name: f.name || f.description || `Пользователь ${f.id?.substring(0, 8) || '?'}`,
      initials: f.initials || getInitials(f.name || f.description),
      color: getRandomColor(f.id || ''),
    }))
  } catch (e) {
    console.error('Failed to load friends:', e)
    friendError.value = e.response?.data?.detail || 'Ошибка при загрузке друзей'
  } finally {
    loadingFriends.value = false
  }
}

// Загрузка текущих распределений
function loadExistingDistributions() {
  participants.value = props.existingDistributions
    .filter(d => d.distribution_status !== 'settled')
    .map(d => ({
      userId: d.user_id || d.userId,
      name: d.user?.name || `Пользователь ${d.user_id?.substring(0, 8) || '?'}`,
      initials: d.user?.initials || getInitials(d.user?.name || ''),
      color: getRandomColor(d.user_id || ''),
      role: d.distribution_user_role,
      size: d.size?.toString() || '',
      isOwner: d.distribution_user_role === 'owner',
      status: d.distribution_status
    }))
}

// Добавить друга
function addFriend(friend) {
  // Проверка, не добавлен ли уже
  if (participants.value.find(p => p.userId === friend.id)) {
    error.value = 'Этот пользователь уже добавлен'
    setTimeout(() => error.value = '', 3000)
    return
  }

  participants.value.push({
    id: friend.id,
    userId: friend.id,
    name: friend.name,
    initials: friend.initials,
    color: friend.color,
    role: 'participant',
    size: '',
    isOwner: false,
    status: 'pending'
  })

  showFriendPicker.value = false
  searchQuery.value = ''
  error.value = ''
}

// Удалить участника
function removeParticipant(index) {
  participants.value.splice(index, 1)
  if (editingIndex.value === index) {
    editingIndex.value = -1
  } else if (editingIndex.value > index) {
    editingIndex.value--
  }
}

// Начать редактирование
function startEdit(index) {
  editingIndex.value = index
  editingSize.value = participants.value[index].size || ''
}

// Сохранить редактирование
function saveEdit(index) {
  const size = parseFloat(editingSize.value)
  if (!isNaN(size) && size >= 0) {
    participants.value[index].size = size
  }
  editingIndex.value = -1
  editingSize.value = ''
}

// Отменить редактирование
function cancelEdit() {
  editingIndex.value = -1
  editingSize.value = ''
}

// Назначить роль владельца
function setOwner(index) {
  // Убираем текущего владельца
  participants.value.forEach((p, i) => {
    if (i !== index) p.role = 'participant'
  })
  participants.value[index].role = 'owner'
}

// Проверка валидности
function validate() {
  if (participants.value.length === 0) {
    error.value = 'Добавьте хотя бы одного участника'
    return false
  }

  // Проверка что есть владелец
  if (!participants.value.some(p => p.role === 'owner')) {
    error.value = 'Необходимо назначить владельца'
    return false
  }

  // Проверка суммы для percentage/amount
  if (splitType.value !== 'equal') {
    const total = participants.value.reduce((sum, p) => sum + (parseFloat(p.size) || 0), 0)
    // Для новой транзакции owner's share считается бэкендом, проверяем что сумма участников <= суммы транзакции
    if (props.isNewTransaction) {
      if (total > props.transactionAmount + 0.01) {
        error.value = `Сумма участников (${total.toFixed(2)}) не может превышать сумму транзакции (${props.transactionAmount.toFixed(2)})`
        return false
      }
    } else {
      if (Math.abs(total - props.transactionAmount) > 0.01) {
        error.value = `Сумма распределения (${total.toFixed(2)}) не совпадает с суммой транзакции (${props.transactionAmount.toFixed(2)})`
        return false
      }
    }
  }

  return true
}

// Сохранить
async function handleSave() {
  if (!validate()) return

  isLoading.value = true
  error.value = ''

  try {
    const distributions = computedSizes.value.map(p => ({
      userId: p.userId,
      transactionId: props.transactionId,
      role: p.role,
      size: parseFloat(p.size) || 0
    }))

    // Для новой транзакции не вызываем API — данные будут отправлены с транзакцией
    if (!props.isNewTransaction) {
      // Отправляем все распределения
      for (const dist of distributions) {
        await distributionApi.add(dist)
      }
    }

    emit('saved')
    // Отправляем полные данные для обновления локального состояния
    emit('update:distributions', computedSizes.value.map(p => ({
      userId: p.userId,
      name: p.name,
      initials: p.initials,
      color: p.color,
      role: p.role,
      size: p.size,
      isOwner: p.isOwner,
      status: p.status,
      splitType: splitType.value
    }))
    )
    closeModal()
  } catch (e) {
    console.error('Failed to save distributions:', e)
    error.value = e.response?.data?.detail || 'Ошибка при сохранении распределений'
  } finally {
    isLoading.value = false
  }
}

function closeModal() {
  emit('update:modelValue', false)
  editingIndex.value = -1
  editingSize.value = ''
  searchQuery.value = ''
  showFriendPicker.value = false
}

function onOpen() {
  loadExistingDistributions()
  loadFriends()
}

watch(() => props.modelValue, (val) => {
  if (val) onOpen()
})

// Сброс при смене типа разделения
watch(splitType, () => {
  if (splitType.value === 'equal' && participants.value.length > 0) {
    // Пересчитываем доли
    const totalPeople = participants.value.length
    const share = Math.round((props.transactionAmount / totalPeople) * 100) / 100
    participants.value.forEach(p => {
      p.size = share.toString()
    })
  }
})

// Форматирование валюты
function formatAmount(amount) {
  const symbols = { RUB: '₽', USD: '$', EUR: '€' }
  const symbol = symbols[props.transactionCurrency] || '₽'
  return `${symbol} ${Math.abs(amount || 0).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

function formatDate(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

function getStatusBadge(status) {
  switch (status) {
    case 'settled':
      return '<span class="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-xs font-medium">✓ Оплачено</span>'
    case 'pending':
      return '<span class="px-2 py-0.5 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded-full text-xs font-medium">⏳ Ожидает</span>'
    default:
      return ''
  }
}
</script>

<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-2xl w-full border border-gray-200 dark:border-gray-700 overflow-hidden animate-fade-in">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900">
        <div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">👥 Распределение расходов</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            Сумма: {{ formatAmount(transactionAmount) }}
          </p>
        </div>
        <button @click="closeModal" class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-red-500 hover:text-white flex items-center justify-center transition-colors">✕</button>
      </div>

      <!-- Split Type Selector -->
      <div class="px-6 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Тип разделения</label>
        <div class="flex gap-2">
          <button
            @click="splitType = 'equal'"
            class="flex-1 px-3 py-2 text-sm font-medium rounded-lg border transition-all"
            :class="splitType === 'equal'
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
              : 'border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-purple-300'"
          >
            ⚖️ Поровну
          </button>
          <button
            @click="splitType = 'amount'"
            class="flex-1 px-3 py-2 text-sm font-medium rounded-lg border transition-all"
            :class="splitType === 'amount'
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
              : 'border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-purple-300'"
          >
            💰 По сумме
          </button>
          <button
            @click="splitType = 'percentage'"
            class="flex-1 px-3 py-2 text-sm font-medium rounded-lg border transition-all"
            :class="splitType === 'percentage'
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
              : 'border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-purple-300'"
          >
            📊 По процентам
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="px-6 py-4 space-y-4 max-h-[60vh] overflow-y-auto">
        <!-- Error -->
        <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-3 rounded-lg text-sm text-red-700 dark:text-red-400">
          {{ error }}
        </div>

        <!-- Participants List -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Участники ({{ participants.length }})</h4>
            <button
              @click="showFriendPicker = !showFriendPicker"
              class="px-3 py-1.5 text-sm bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors flex items-center gap-1"
            >
              ➕ Добавить
            </button>
          </div>

          <!-- Friend Picker -->
          <div v-if="showFriendPicker" class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 bg-gray-50 dark:bg-gray-900/50 space-y-3">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="🔍 Поиск по имени..."
              />
            </div>

            <div v-if="loadingFriends" class="text-center py-4 text-gray-400">
              Загрузка друзей...
            </div>
            <div v-else-if="friendError" class="text-center py-2 text-red-500 text-sm">
              {{ friendError }}
            </div>
            <div v-else-if="filteredFriends.length === 0" class="text-center py-2 text-gray-400 text-sm">
              Друзья не найдены
            </div>
            <div v-else class="max-h-40 overflow-y-auto space-y-1">
              <button
                v-for="friend in filteredFriends"
                :key="friend.id"
                @click="addFriend(friend)"
                class="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors text-left"
              >
                <div :class="[friend.color, 'w-8 h-8 rounded-full flex items-center justify-center font-bold text-white text-xs']">
                  {{ friend.initials }}
                </div>
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ friend.name }}</span>
                <span class="ml-auto text-xs text-purple-600 dark:text-purple-400 font-medium">Добавить</span>
              </button>
            </div>
          </div>

          <!-- Participants -->
          <div v-if="participants.length === 0" class="text-center py-8 text-gray-400 dark:text-gray-500">
            <p class="text-3xl mb-2">👥</p>
            <p class="text-sm">Нажмите "Добавить" чтобы добавить участников</p>
          </div>

          <div v-for="(p, index) in participants" :key="p.userId" class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 bg-gray-50 dark:bg-gray-900/50">
            <div class="flex items-center gap-3">
              <!-- Avatar -->
              <div :class="[p.color, 'w-10 h-10 rounded-full flex items-center justify-center font-bold text-white text-sm flex-shrink-0']">
                {{ p.initials }}
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-medium text-gray-900 dark:text-gray-100 truncate">{{ p.name }}</span>
                  <span v-if="p.isOwner" class="px-2 py-0.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded text-xs font-medium">
                    👑 Владелец
                  </span>
                </div>
                <div class="flex items-center gap-2 mt-0.5">
                  <span v-html="getStatusBadge(p.status)" />
                  <button
                    v-if="!p.isOwner"
                    @click="setOwner(index)"
                    class="text-xs text-amber-600 hover:text-amber-700 dark:text-amber-400 hover:underline"
                  >
                    Сделать владельцем
                  </button>
                </div>
              </div>

              <!-- Size input -->
              <div class="flex items-center gap-2 flex-shrink-0">
                <template v-if="splitType === 'equal'">
                  <span class="text-sm font-mono font-semibold text-purple-600 dark:text-purple-400">
                    {{ formatAmount(p.size) }}
                  </span>
                </template>
                <template v-else>
                  <input
                    v-if="editingIndex === index"
                    v-model="editingSize"
                    type="number"
                    step="0.01"
                    class="w-24 px-2 py-1 border border-purple-400 rounded text-sm font-mono bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    v-else
                    @click="startEdit(index)"
                    class="w-24 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono text-gray-900 dark:text-gray-100 hover:bg-white dark:hover:bg-gray-800 text-right"
                  >
                    {{ formatAmount(p.size) }}
                  </button>
                </template>
              </div>

              <!-- Actions -->
              <button
                @click="removeParticipant(index)"
                class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors flex-shrink-0"
                title="Удалить"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div v-if="participants.length > 0" class="border-t border-gray-200 dark:border-gray-700 pt-3 space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-500 dark:text-gray-400">Сумма транзакции:</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100">{{ formatAmount(transactionAmount) }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-500 dark:text-gray-400">Распределено:</span>
            <span class="font-semibold text-purple-600 dark:text-purple-400">{{ formatAmount(totalDistributed) }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-500 dark:text-gray-400">Остаток:</span>
            <span :class="['font-semibold', remainder === 0 ? 'text-green-600' : 'text-orange-500']">
              {{ formatAmount(remainder) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex gap-3 bg-gray-50 dark:bg-gray-900/50">
        <button
          @click="handleSave"
          :disabled="isLoading"
          class="flex-1 px-4 py-2.5 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
        >
          <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
          </svg>
          {{ isLoading ? 'Сохранение...' : 'Сохранить распределение' }}
        </button>
        <button
          @click="closeModal"
          class="px-4 py-2.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors"
        >
          Отмена
        </button>
      </div>
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
