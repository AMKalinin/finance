import axios from 'axios'
import { settings } from '../config/settings.js'

// Настройка базового URL для всех запросов
axios.defaults.baseURL = settings.backend.baseUrl
axios.defaults.timeout = settings.backend.timeout

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const finApi = {
  async getAccounts(skip = 0, limit = 100) {
    return axios.get('/account/', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching accounts:', error); throw error })
  },

  async getCategories(skip = 0, limit = 100) {
    return axios.get('/category/', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching categories:', error); throw error })
  },

  async getExpenseCategories(skip = 0, limit = 100) {
    return axios.get('/category/type/expenses', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching expense categories:', error); throw error })
  },

  async getIncomeCategories(skip = 0, limit = 100) {
    return axios.get('/category/type/income', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching income categories:', error); throw error })
  },

  async getTransactions(skip = 0, limit = 100) {
    return axios.get('/transaction/all', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching transactions:', error); throw error })
  },

  async getTransactionsByPeriod(fromDate, toDate, skip = 0, limit = 100) {
    return axios.get('/transaction/by_period', { params: { from_date: fromDate, to_date: toDate, skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching transactions by period:', error); throw error })
  },

  async getPrimaryAccounts(skip = 0, limit = 100) {
    return axios.get('/account/primary', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching primary accounts:', error); throw error })
  },

  async getArchivedAccounts(skip = 0, limit = 100) {
    return axios.get('/account/archived', { params: { skip, limit } }).then((response) => response.data).catch(error => { console.error('Error fetching archived accounts:', error); throw error })
  },

  async createAccount(account) {
    const payload = {
      name: account.name,
      currency: account.currency || 'RUB',
      balance: account.balance || 0,
      description: account.description || '',
      interest_rate: account.interestRate || null,
      is_emergency_fund: account.isEmergencyFund || false,
      decimal_places: account.decimalPlaces || 2,
      is_archived: account.isArchived || false,
      is_primary: account.isPrimary || false,
      account_type: account.accountType || 'checking'
    }
    return axios.post('/account/create', payload).then((response) => response.data).catch(error => { console.error('Error creating account:', error); throw error })
  },

  async updateAccountBalance(id, operation, balance) {
    return axios.put(`/account/${id}/balance`, {
      id,
      operation,
      balance
    }).then((response) => response.data).catch(error => { console.error('Error updating account balance:', error); throw error })
  },

  async updateAccountName(id, name) {
    return axios.put(`/account/${id}/name`, {
      id,
      name
    }).then((response) => response.data).catch(error => { console.error('Error updating account name:', error); throw error })
  },

  async updateAccountDescription(id, description) {
    return axios.put(`/account/${id}/description`, {
      id,
      description
    }).then((response) => response.data).catch(error => { console.error('Error updating account description:', error); throw error })
  },

  async updateAccountInterestRate(id, interestRate) {
    return axios.put(`/account/${id}/interest_rate`, {
      id,
      interest_rate: interestRate
    }).then((response) => response.data).catch(error => { console.error('Error updating account interest rate:', error); throw error })
  },

  async updateAccountEmergencyFund(id, isEmergencyFund) {
    return axios.put(`/account/${id}/emergency_fund`, {
      id,
      is_emergency_fund: isEmergencyFund
    }).then((response) => response.data).catch(error => { console.error('Error updating account emergency fund:', error); throw error })
  },

  async updateAccountDecimalPlaces(id, decimalPlaces) {
    return axios.put(`/account/${id}/decimal_places`, {
      id,
      decimal_places: decimalPlaces
    }).then((response) => response.data).catch(error => { console.error('Error updating account decimal places:', error); throw error })
  },

  async updateAccountArchived(id, isArchived) {
    return axios.put(`/account/${id}/archived`, {
      id,
      is_archived: isArchived
    }).then((response) => response.data).catch(error => { console.error('Error updating account archived status:', error); throw error })
  },

  async updateAccountPrimary(id, isPrimary) {
    return axios.put(`/account/${id}/primary`, {
      id,
      is_primary: isPrimary
    }).then((response) => response.data).catch(error => { console.error('Error updating account primary status:', error); throw error })
  },

  async getAccountById(id) {
    return axios.get(`/account/${id}`).then((response) => response.data).catch(error => { console.error('Error fetching account by id:', error); throw error })
  },

  async deleteAccount(id) {
    return axios.delete(`/account/${id}`).then((response) => response.data).catch(error => { console.error('Error deleting account:', error); throw error })
  },

  async createCategory(category) {
    const payload = {
      name: category.name,
      type: category.type || null,
      parentCategory: category.parentCategory || null,
      level: category.level || 1
    }
    return axios.post('/category/create', payload).then((response) => response.data).catch(error => { console.error('Error creating category:', error); throw error })
  },

  async updateCategoryName(id, name) {
    return axios.put(`/category/${id}/name`, {
      id,
      name
    }).then((response) => response.data).catch(error => { console.error('Error updating category name:', error); throw error })
  },

  async deleteCategory(id) {
    return axios.delete(`/category/${id}`).then((response) => response.data).catch(error => { console.error('Error deleting category:', error); throw error })
  },

  async createTransaction(transaction) {
    const payload = {
      FROM: transaction.FROM || null,
      TO: transaction.TO || null,
      category: transaction.category || null,
      type: transaction.type || 'debit',
      debitSize: transaction.debitSize || transaction.size,
      creditSize: transaction.creditSize || null,
      exchangeRate: transaction.exchangeRate || 1,
      date: transaction.date,
      description: transaction.description || '',
      splitType: transaction.splitType || null,
      status: transaction.status || 'settled',
      relatedTransaction: transaction.relatedTransaction || null,
      distributions: transaction.distributions || [],
      positions: transaction.positions || []
    }
    return axios.post('/transaction/create', payload).then((response) => response.data).catch(error => { console.error('Error creating transaction:', error); throw error })
  },

  async createDistribution(distributionInfo) {
    return axios.post('/transaction/distribution', distributionInfo).then((response) => response.data).catch(error => { console.error('Error adding distribution:', error); throw error })
  },

  async updateDistribution(distributionInfo) {
    return axios.patch('/transaction/distribution', distributionInfo).then((response) => response.data).catch(error => { console.error('Error updating distribution:', error); throw error })
  },

  async deleteDistribution(distributionInfo) {
    return axios.delete('/transaction/distribution', { data: distributionInfo }).then((response) => response.data).catch(error => { console.error('Error deleting distribution:', error); throw error })
  },

  async settleDistribution(settleInfo) {
    return axios.patch('/transaction/distribution/settle', settleInfo).then((response) => response.data).catch(error => { console.error('Error settling distribution:', error); throw error })
  },

  async addPosition(positionInfo) {
    return axios.post('/transaction/position', positionInfo).then((response) => response.data).catch(error => { console.error('Error adding position:', error); throw error })
  },

  async updatePosition(positionInfo) {
    return axios.patch('/transaction/position', positionInfo).then((response) => response.data).catch(error => { console.error('Error updating position:', error); throw error })
  },

  async updateTransactionDate(id, date) {
    return axios.put(`/transaction/${id}/date`, { id, date }).then((response) => response.data).catch(error => { console.error('Error updating transaction date:', error); throw error })
  },

  async updateTransactionSize(id, size) {
    return axios.put(`/transaction/${id}/size`, { id, size }).then((response) => response.data).catch(error => { console.error('Error updating transaction size:', error); throw error })
  },

  async updateTransactionDescription(id, description) {
    return axios.put(`/transaction/${id}/description`, { id, description }).then((response) => response.data).catch(error => { console.error('Error updating transaction description:', error); throw error })
  },

  async deleteTransaction(id) {
    return axios.delete(`/transaction/${id}`).then((response) => response.data).catch(error => { console.error('Error deleting transaction:', error); throw error })
  },

  async getUserInfo() {
    return axios.get('/user/info').then((response) => response.data).catch(error => { console.error('Error fetching user info:', error); throw error })
  },

  async getFriends() {
    return axios.get('/user/friends').then((response) => response.data).catch(error => { console.error('Error fetching friends:', error); throw error })
  }
}
