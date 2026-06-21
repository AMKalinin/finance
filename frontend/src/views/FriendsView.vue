<script setup>
import { ref, computed, onMounted } from 'vue'
import { friendApi } from '@/api/client'
import { useLanguageStore } from '@/stores/languageStore'
import CreateFriendModal from '@/components/Modals/CreateFriendModal.vue'

const { t } = useLanguageStore()

const activeTab = ref('friends') // 'friends' | 'received' | 'sent'

const friends = ref([])
const receivedRequests = ref([])
const sentRequests = ref([])
const isLoading = ref(false)
const error = ref('')

const showAddFriendModal = ref(false)
const showEditRequestModal = ref(false)
const editData = ref(null)

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

function formatDate(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function loadFriends() {
  isLoading.value = true
  error.value = ''
  try {
    const res = await friendApi.getAll()
    const data = res.data?.items || res.data?.friends || res.data || []
    friends.value = data.map(f => ({
      id: f.id,
      name: f.name || f.description || `Пользователь ${f.id?.substring(0, 8) || '?'}`,
      initials: f.initials || getInitials(f.name || f.description),
      color: getRandomColor(f.id || ''),
      status: f.status,
      created_at: f.created_at
    }))
  } catch (e) {
    console.error('Failed to load friends:', e)
    error.value = e.response?.data?.detail || 'Ошибка при загрузке друзей'
  } finally {
    isLoading.value = false
  }
}

async function loadReceivedRequests() {
  isLoading.value = true
  error.value = ''
  try {
    const res = await friendApi.getRequests()
    const data = res.data?.items || res.data?.requests || res.data || []
    receivedRequests.value = data.map(r => ({
      id: r.id,
      name: r.name || r.description || `Пользователь ${r.id?.substring(0, 8) || '?'}`,
      initials: r.initials || getInitials(r.name || r.description),
      color: getRandomColor(r.id || ''),
      status: r.status,
      created_at: r.created_at
    }))
  } catch (e) {
    console.error('Failed to load received requests:', e)
    error.value = e.response?.data?.detail || 'Ошибка при загрузке входящих запросов'
  } finally {
    isLoading.value = false
  }
}

async function loadSentRequests() {
  isLoading.value = true
  error.value = ''
  try {
    const res = await friendApi.getSentRequests()
    const data = res.data?.items || res.data?.requests || res.data || []
    sentRequests.value = data.map(r => ({
      id: r.id,
      name: r.name || r.description || `Пользователь ${r.id?.substring(0, 8) || '?'}`,
      initials: r.initials || getInitials(r.name || r.description),
      color: getRandomColor(r.id || ''),
      status: r.status,
      created_at: r.created_at
    }))
  } catch (e) {
    console.error('Failed to load sent requests:', e)
    error.value = e.response?.data?.detail || 'Ошибка при загрузке отправленных запросов'
  } finally {
    isLoading.value = false
  }
}

async function loadAll() {
  await Promise.all([loadFriends(), loadReceivedRequests(), loadSentRequests()])
}

async function acceptRequest(requestId) {
  error.value = ''
  try {
    await friendApi.acceptRequest(requestId)
    await loadAll()
  } catch (e) {
    console.error('Failed to accept request:', e)
    error.value = e.response?.data?.detail || 'Ошибка при подтверждении запроса'
  }
}

async function declineRequest(requestId) {
  error.value = ''
  try {
    await friendApi.declineRequest(requestId)
    await loadAll()
  } catch (e) {
    console.error('Failed to decline request:', e)
    error.value = e.response?.data?.detail || 'Ошибка при отклонении запроса'
  }
}

async function removeFriend(friendId) {
  error.value = ''
  try {
    await friendApi.removeFriend(friendId)
    await loadAll()
  } catch (e) {
    console.error('Failed to remove friend:', e)
    error.value = e.response?.data?.detail || 'Ошибка при удалении друга'
  }
}

function openEditModal(request) {
  editData.value = {
    id: request.id,
    status: request.status
  }
  showEditRequestModal.value = true
}

async function onModalSaved() {
  await loadAll()
}

onMounted(() => {
  loadAll()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Друзья</h2>
      <button
        @click="showAddFriendModal = true"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Добавить друга
      </button>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-gray-200 dark:border-gray-700">
      <button
        @click="activeTab = 'friends'"
        class="px-4 py-3 text-sm font-medium transition-colors border-b-2"
        :class="activeTab === 'friends'
          ? 'border-blue-600 text-blue-600 dark:text-blue-400'
          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'"
      >
        Друзья
        <span v-if="friends.length" class="ml-2 px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full">
          {{ friends.length }}
        </span>
      </button>
      <button
        @click="activeTab = 'received'"
        class="px-4 py-3 text-sm font-medium transition-colors border-b-2"
        :class="activeTab === 'received'
          ? 'border-blue-600 text-blue-600 dark:text-blue-400'
          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'"
      >
        Входящие запросы
        <span v-if="receivedRequests.length" class="ml-2 px-2 py-0.5 text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded-full">
          {{ receivedRequests.length }}
        </span>
      </button>
      <button
        @click="activeTab = 'sent'"
        class="px-4 py-3 text-sm font-medium transition-colors border-b-2"
        :class="activeTab === 'sent'
          ? 'border-blue-600 text-blue-600 dark:text-blue-400'
          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'"
      >
        Отправленные запросы
        <span v-if="sentRequests.length" class="ml-2 px-2 py-0.5 text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full">
          {{ sentRequests.length }}
        </span>
      </button>
    </div>

    <!-- Error message -->
    <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-4 rounded-lg text-sm text-red-700 dark:text-red-400">
      {{ error }}
      <button @click="error = ''" class="ml-2 underline">Закрыть</button>
    </div>

    <!-- Friends Tab -->
    <div v-if="activeTab === 'friends'">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="friends.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-3">👥</div>
        <p class="text-lg font-medium">У вас пока нет друзей</p>
        <p class="text-sm mt-1">Пригласите кого-нибудь, нажав кнопку "Добавить друга"</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="friend in friends"
          :key="friend.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3"
        >
          <div
            :class="[friend.color, 'w-12 h-12 rounded-full flex items-center justify-center font-bold text-white text-lg']"
          >
            {{ friend.initials }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="font-semibold text-gray-900 dark:text-gray-100 truncate">{{ friend.name }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              ID: {{ friend.id?.substring(0, 8) }}...
            </div>
          </div>
          <button
            @click="removeFriend(friend.id)"
            class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
            title="Удалить из друзей"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Received Requests Tab -->
    <div v-if="activeTab === 'received'">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="receivedRequests.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-3">📭</div>
        <p class="text-lg font-medium">Нет входящих запросов</p>
        <p class="text-sm mt-1">Запросы от друзей будут появляться здесь</p>
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="req in receivedRequests"
          :key="req.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-4"
        >
          <div
            :class="[req.color, 'w-12 h-12 rounded-full flex items-center justify-center font-bold text-white text-lg']"
          >
            {{ req.initials }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="font-semibold text-gray-900 dark:text-gray-100">{{ req.name }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              Запрос от {{ formatDate(req.created_at) }}
            </div>
          </div>
          <div class="flex gap-2">
            <button
              @click="acceptRequest(req.id)"
              class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium text-sm transition-colors flex items-center gap-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Принять
            </button>
            <button
              @click="declineRequest(req.id)"
              class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 rounded-lg font-medium text-sm transition-colors flex items-center gap-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Отклонить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sent Requests Tab -->
    <div v-if="activeTab === 'sent'">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="sentRequests.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-3">📤</div>
        <p class="text-lg font-medium">Нет отправленных запросов</p>
        <p class="text-sm mt-1">Отправьте запрос кому-нибудь, нажав кнопку "Добавить друга"</p>
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="req in sentRequests"
          :key="req.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-4"
        >
          <div
            :class="[req.color, 'w-12 h-12 rounded-full flex items-center justify-center font-bold text-white text-lg']"
          >
            {{ req.initials }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="font-semibold text-gray-900 dark:text-gray-100">{{ req.name }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              Запрос отправлен {{ formatDate(req.created_at) }}
            </div>
            <div class="mt-1 px-2 py-0.5 inline-block text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded">
              Ожидает подтверждения
            </div>
          </div>
          <button
            @click="openEditModal(req)"
            class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 rounded-lg font-medium text-sm transition-colors"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>

    <!-- Add Friend Modal -->
    <CreateFriendModal
      v-model="showAddFriendModal"
      @saved="onModalSaved"
    />

    <!-- Edit Request Modal (accept/decline) -->
    <CreateFriendModal
      v-model="showEditRequestModal"
      :edit-data="editData"
      @saved="onModalSaved"
    />
  </div>
</template>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
