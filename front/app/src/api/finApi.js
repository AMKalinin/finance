import axios from 'axios'


const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const finApi = {
  async getAccounts() {
    return axios.get('/account/').then((response) => response.data).catch(error =>{console.log('fff')})
  },

  async getCategories() {
    return axios.get('/category/').then((response) => response.data).catch(error =>{console.log('fff')})
  },

  async getTransactions() {
    return axios.get('/transaction/all').then((response) => response.data).catch(error =>{console.log('fff')})
  },

  async createAccount(account) {
    return axios.post('/account/create',
      {
        name: account.name,
        currency: 'RUB',
        balance: account.balance,
        description: 'testi'
      }).then((response) => response.data).catch(error =>{console.log('fff')})
  },

  async createCategory(category) {
    return axios.post('/category/create',
      {
        name: category.name,
        typeCategory: category.type
      }).then((response) => response.data)
  },

  async createTransaction(transaction) {
    return axios.post('/transaction/create', transaction).then((response) => response.data)
  },

  async deleteAccount(id) {
    await delay(300)
  },

  async deleteCategory(id) {
    await delay(300)
  }
}
