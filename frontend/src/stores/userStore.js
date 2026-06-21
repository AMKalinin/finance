import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { userApi, friendApi } from '@/api/client'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(null)
  const friends = ref([])
  const receivedRequests = ref([])
  const sentRequests = ref([])
  const isLoading = ref(false)
  const error = ref('')

  async function fetchUserInfo() {
    isLoading.value = true
    error.value = ''
    try {
      const response = await userApi.getInfo()
      userInfo.value = response.data || response
    } catch (e) {
      console.error('Failed to fetch user info:', e)
      userInfo.value = null
      error.value = e.response?.data?.detail || 'Ошибка при загрузке информации о пользователе'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchFriends() {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.getAll()
      const data = response.data?.items || response.data?.friends || response.data || []
      friends.value = data
    } catch (e) {
      console.error('Failed to fetch friends:', e)
      friends.value = []
      error.value = e.response?.data?.detail || 'Ошибка при загрузке друзей'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchReceivedRequests() {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.getRequests()
      const data = response.data?.items || response.data?.requests || response.data || []
      receivedRequests.value = data
    } catch (e) {
      console.error('Failed to fetch received requests:', e)
      receivedRequests.value = []
      error.value = e.response?.data?.detail || 'Ошибка при загрузке входящих запросов'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchSentRequests() {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.getSentRequests()
      const data = response.data?.items || response.data?.requests || response.data || []
      sentRequests.value = data
    } catch (e) {
      console.error('Failed to fetch sent requests:', e)
      sentRequests.value = []
      error.value = e.response?.data?.detail || 'Ошибка при загрузке отправленных запросов'
    } finally {
      isLoading.value = false
    }
  }

  async function addFriend(friendId) {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.create(friendId)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка при отправке запроса'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function acceptRequest(requestId) {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.acceptRequest(requestId)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка при подтверждении запроса'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function declineRequest(requestId) {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.declineRequest(requestId)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка при отклонении запроса'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function removeFriend(friendId) {
    isLoading.value = true
    error.value = ''
    try {
      const response = await friendApi.removeFriend(friendId)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка при удалении друга'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function refreshAll() {
    await Promise.all([
      fetchFriends(),
      fetchReceivedRequests(),
      fetchSentRequests(),
    ])
  }

  return {
    userInfo,
    friends,
    receivedRequests,
    sentRequests,
    isLoading,
    error,
    fetchUserInfo,
    fetchFriends,
    fetchReceivedRequests,
    fetchSentRequests,
    addFriend,
    acceptRequest,
    declineRequest,
    removeFriend,
    refreshAll,
  }
})
