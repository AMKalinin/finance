import axios from 'axios'


const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const finApi = {
  async getAccounts() {
    return axios.get('http://192.168.0.24:8001/api/v1/account/').then((response) => response.data)
  },

  async getCategories() {
    return axios.get('http://192.168.0.24:8001/api/v1/category/').then((response) => response.data)
  },

  async getTransactions() {
    return axios.get('http://192.168.0.24:8001/api/v1/transaction/all').then((response) => response.data)
  },

  async createAccount(account) {
    return axios.post('http://192.168.0.24:8001/api/v1/account/create',
      {
        name: account.name,
        currency: 'RUB',
        balance: account.balance,
        description: 'testi'
      }).then((response) => response.data)
  },

  async createCategory(category) {
    return axios.post('http://192.168.0.24:8001/api/v1/category/create',
      {
        name: category.name,
        typeCategory: category.type
      }).then((response) => response.data)
  },

  async createTransaction(transaction) {
    return axios.post('http://192.168.0.24:8001/api/v1/transaction/create', transaction).then((response) => response.data)
  },

  async deleteAccount(id) {
    await delay(300)
  },

  async deleteCategory(id) {
    await delay(300)
  }
}
