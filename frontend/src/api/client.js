import axios from 'axios'
import { getToken, isUserAuthenticated } from '@/keycloak/keycloak-init'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Логирование запросов и ответов для отладки
apiClient.interceptors.request.use(
  async (config) => {
    const token = await getToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Добавляем логирование запросов в консоль
    console.log('📡 REQUEST:', {
      url: config.url,
      method: config.method,
      params: config.params,
      headers: Object.fromEntries(Object.entries(config.headers).filter(([k]) => !k.startsWith('__')))
    })
    
    return config
  },
  (error) => Promise.reject(error)
)

apiClient.interceptors.response.use(
  (response) => {
    // Логирование успешных ответов
    console.log('✅ RESPONSE:', {
      url: response.config.url,
      status: response.status,
      dataLength: JSON.stringify(response.data).length
    })
    return response
  },
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    } else if (!navigator.onLine) {
      console.warn('⚠️ No internet connection. Queueing request.')
      return queueRequest(error.config)
    }
    return Promise.reject(error)
  }
)

let retryTimeout = null

const processQueue = async () => {
  if (retryTimeout) clearTimeout(retryTimeout)

  retryTimeout = setTimeout(async () => {
    while (requestQueue.length > 0) {
      const { config, resolve, reject } = requestQueue.shift()
      try {
        const response = await apiClient(config)
        resolve(response)
      } catch (error) {
        reject(error)
      }
    }
    retryTimeout = null
  }, 3000)
}

window.addEventListener('online', processQueue)

const requestQueue = []

const queueRequest = (config) => {
  return new Promise((resolve, reject) => {
    requestQueue.push({ config, resolve, reject })
  })
}

export const accountApi = {
  getAll: async (params = {}) => {
    console.log('📊 Loading accounts...')
    const response = await apiClient.get('/account/', { params })
    
    // Обработка разных форматов ответа от API
    const data = response.data || {}
    return {
      ...response,
      data: {
        items: (data.items || data) || [],
        total: data.total || 0,
        totalPages: Math.ceil((data.total || 0) / (params?.limit || 20))
      }
    }
  },
  getById: async (id) => apiClient.get(`/account/${id}`),
  create: async (data) => apiClient.post('/account/create', data),
  updateName: async (id, name) => apiClient.put(`/account/${id}/name`, { name }),
  updateBalance: async (id, operation, balance) => apiClient.put(`/account/${id}/balance`, { id, operation, balance }),
  updateDescription: async (id, description) => apiClient.put(`/account/${id}/description`, { id, description }),
  updateInterestRate: async (id, interestRate) => apiClient.put(`/account/${id}/interest_rate`, { id, interest_rate: interestRate }),
  updateArchived: async (id, isArchived) => apiClient.put(`/account/${id}/archived`, { id, is_archived: isArchived }),
  updatePrimary: async (id, isPrimary) => apiClient.put(`/account/${id}/primary`, { id, is_primary: isPrimary }),
  archive: async (id) => apiClient.put(`/account/${id}/archived`, { id, is_archived: true }),
  restore: async (id) => apiClient.put(`/account/${id}/archived`, { id, is_archived: false }),
  archived: async (params = {}) => {
    const response = await apiClient.get('/account/archived', { params })
    return response
  },
  primary: async (params = {}) => {
    const response = await apiClient.get('/account/primary', { params })
    return response
  },
  delete: async (id) => apiClient.delete(`/account/${id}`),
  // Маппинг snake_case -> camelCase для бэкенда
  mapToBackend(account) {
    return {
      name: account.name,
      currency: account.currency,
      balance: account.balance,
      description: account.description,
      interest_rate: account.interestRate,
      is_emergency_fund: account.isEmergencyFund || false,
      decimal_places: account.decimalPlaces || 2,
      is_archived: account.archived || false,
      is_primary: account.isPrimary || false,
      account_type: account.type,
    }
  },
  // Маппинг camelCase -> snake_case для ответа бэкенда
  mapFromBackend(account) {
    if (!account) return account
    return {
      id: account.id,
      name: account.name,
      type: account.account_type || account.accountType,
      currency: account.currency,
      balance: account.balance,
      description: account.description,
      interestRate: account.interest_rate || account.interestRate,
      isPrimary: account.is_primary || account.isPrimary,
      archived: account.is_archived || account.isArchived,
      isEmergencyFund: account.is_emergency_fund || false,
      decimalPlaces: account.decimal_places || 2,
    }
  },
}

export const transactionApi = {
  // Маппинг snake_case -> camelCase для ответа бэкенда
  mapFromBackend(txn, accountsMap, categoriesMap) {
    if (!txn) return txn
    const fromAccount = accountsMap?.get(txn.from_account_id)
    const toAccount = accountsMap?.get(txn.to_account_id)
    const category = categoriesMap?.get(txn.category)
    
    console.log('📊 Transaction mapped:', {
      id: txn.id,
      type: txn.type,
      fromAccountId: txn.from_account_id,
      toAccountId: txn.to_account_id,
      categoryId: txn.category,
      debitSize: txn.debit_size,
      creditSize: txn.credit_size,
    })
    
    return {
      id: txn.id,
      type: txn.type,
      fromAccountId: txn.from_account_id,
      toAccountId: txn.to_account_id,
      categoryId: txn.category,
      debitSize: txn.debit_size,
      creditSize: 0,
      amount: txn.type === 'adding' ? (txn.credit_size || 0) : -(txn.debit_size || 0),
      currency: 'RUB',
      date: txn.date ? (typeof txn.date === 'string' ? txn.date : txn.date.toISOString().split('T')[0]) : '',
      description: txn.description,
      status: txn.status,
      distributions: txn.transaction_distribution_user || txn.distributions || [],
      positions: txn.positions || [],
      exchangeRate: txn.exchange_rate,
      splitType: txn.split_type,
      relatedTransaction: txn.related_transaction,
      name: txn.description || 'Без описания',
      account: toAccount || fromAccount || null,
      category: category ? { id: txn.category, name: category.name, icon: category.icon, type: category.type } : null
    }
  },
  // Маппинг camelCase -> snake_case для запроса бэкенду
  mapToBackend(data) {
    if (!data) return data
    const result = {}
    if (data.type) result.type = data.type
    if (data.fromAccountId) result.FROM = data.fromAccountId
    if (data.toAccountId) result.TO = data.toAccountId
    if (data.categoryId) result.category = data.categoryId
    if (data.type === 'debit') {
      result.debit_size = Math.abs(data.amount)
      result.credit_size = null
    } else if (data.type === 'adding') {
      result.debit_size = null
      result.credit_size = Math.abs(data.amount)
    } else if (data.type === 'transfer') {
      result.debit_size = Math.abs(data.amount)
      result.credit_size = Math.abs(data.amount)
    }
    if (data.date) result.date = data.date
    if (data.description != null) result.description = data.description
    if (data.status) result.status = data.status
    // По умолчанию settled, если статус не указан
    if (!result.status) result.status = 'settled'
    return result
  },
  getAll: async (params = {}) => {
    console.log('📊 Loading transactions...')
    const response = await apiClient.get('/transaction/all', { params })
    const data = response.data || {}
    
    // Обработка разных форматов ответа от API
    return {
      ...response,
      data: {
        items: (data.items || data) || [],
        total: data.total || 0,
        totalPages: Math.ceil((data.total || 0) / (params?.limit || 20))
      }
    }
  },
  getByPeriod: async (startDate, endDate, params = {}) => {
    const allParams = { from_date: startDate, to_date: endDate, ...params }
    console.log('📊 Loading transactions by period...', allParams)
    const response = await apiClient.get('/transaction/by_period', { params: allParams })
    const data = response.data || {}
    
    return {
      ...response,
      data: {
        items: (data.items || data) || [],
        total: data.total || 0,
        totalPages: Math.ceil((data.total || 0) / (params?.limit || 20))
      }
    }
  },
  getByPeriodWithType: async (startDate, endDate, type, params = {}) => {
    const allParams = { from_date: startDate, to_date: endDate, operation_type: type, ...params }
    console.log('📊 Loading transactions by period and type...', allParams)
    const response = await apiClient.get('/transaction/by_period', { params: allParams })
    const data = response.data || {}
    
    return {
      ...response,
      data: {
        items: (data.items || data) || [],
        total: data.total || 0,
        totalPages: Math.ceil((data.total || 0) / (params?.limit || 20))
      }
    }
  },
  create: async (data) => {
    console.log('📊 Creating transaction...', data)
    const response = await apiClient.post('/transaction/create', data)
    return { ...response, data: response.data }
  },
  update: async (id, data) => {
    console.log('📊 Updating transaction:', id, data)
    const response = await apiClient.put(`/transaction/${id}`, data)
    return { ...response, data: response.data }
  },
  updateDate: async (id, date) => apiClient.put(`/transaction/${id}/date`, { date }),
  updateSize: async (id, size) => apiClient.put(`/transaction/${id}/size`, { size }),
  updateDescription: async (id, description) => apiClient.put(`/transaction/${id}/description`, { description }),
  delete: async (id) => apiClient.delete(`/transaction/${id}`),
}

export const categoryApi = {
  getAll: async (skip = 0, limit = 100) => {
    console.log('📁 Loading categories...')
    const response = await apiClient.get('/category/', { params: { skip, limit } })
    
    // Обработка разных форматов ответа от API
    const data = response.data || {}
    return {
      ...response,
      data: {
        items: (data.items || data) || [],
        total: data.total || 0,
        totalPages: Math.ceil((data.total || 0) / (limit || 100))
      }
    }
  },
  getExpenses: async (skip = 0, limit = 100) => {
    const response = await apiClient.get('/category/type/expenses', { params: { skip, limit } })
    return response
  },
  getIncome: async (skip = 0, limit = 100) => {
    const response = await apiClient.get('/category/type/income', { params: { skip, limit } })
    return response
  },
  create: async (data) => apiClient.post('/category/create', data),
  updateName: async (id, name) => apiClient.put(`/category/${id}/name`, { id, name }),
  delete: async (id) => apiClient.delete(`/category/${id}`),
}

export const userApi = {
  getInfo: async () => apiClient.get('/user/info'),
  getFriends: async () => apiClient.get('/user/friends'),
}

export const friendApi = {
  getAll: async () => apiClient.get('/user/friends'),
  getRequests: async () => apiClient.get('/user/friend-requests'),
  getSentRequests: async () => apiClient.get('/user/friend-requests/sent'),
  create: async (friendId) => apiClient.post('/user/friend', { friend_id: friendId }),
  acceptRequest: async (requestId) => apiClient.put('/user/friend/accept', { friend_id: requestId }),
  declineRequest: async (requestId) => apiClient.put('/user/friend/reject', { friend_id: requestId }),
  cancelSentRequest: async (friendId) => apiClient.put('/user/friend/cancel-sent', { friend_id: friendId }),
  removeFriend: async (friendId) => apiClient.delete('/user/friend', { data: { friend_id: friendId } }),
  delete: async (friendId) => friendApi.removeFriend(friendId),
}

export default apiClient
