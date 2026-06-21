<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { login, getToken, isUserAuthenticated } from '@/keycloak/keycloak-init'

const router = useRouter()
const { t } = useI18n()
const isLoading = ref(false)
const error = ref('')

async function handleLogin() {
  try {
    isLoading.value = true
    error.value = ''
    await login()
  } catch (err) {
    console.error('Login error:', err)
    error.value = t('common.loginKeycloak') + ' failed'
  } finally {
    isLoading.value = false
  }
}

async function checkAuth() {
  try {
    const token = await getToken()
    if (token && isUserAuthenticated()) {
      router.push('/')
    }
  } catch (error) {
    console.error('Auth check error:', error)
  }
}

onMounted(checkAuth)
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 px-4">
    <div class="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 space-y-8 transition-colors duration-200 border border-gray-200 dark:border-gray-700">
      <div class="text-center">
        <div class="w-16 h-16 mx-auto bg-gradient-to-br from-blue-600 to-blue-500 rounded-xl flex items-center justify-center text-white text-3xl font-bold shadow-lg mb-4">₿</div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">FinanceApp</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Управление личными финансами</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-4 rounded-lg">
          <p class="text-sm text-red-700 dark:text-red-400">{{ error }}</p>
        </div>

        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 space-y-3 border border-gray-200 dark:border-gray-600">
          <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            {{ t('common.securityAuth') }}
          </h3>
          <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li class="flex items-start gap-2">
              <span class="text-green-600 mt-0.5">✓</span>
              <span>{{ t('common.sso') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-600 mt-0.5">✓</span>
              <span>{{ t('common.autoTokenUpdate') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-600 mt-0.5">✓</span>
              <span>{{ t('common.secureStorage') }}</span>
            </li>
          </ul>
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <svg v-if="!isLoading" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
          </svg>
          {{ isLoading ? t('common.loading') : t('common.loginKeycloak') }}
        </button>

        <div class="text-center text-sm text-gray-600 dark:text-gray-400">
          <p>Авторизация через Keycloak SSO</p>
        </div>
      </form>

      <div class="pt-6 border-t border-gray-200 dark:border-gray-700 text-center">
        <p class="text-xs text-gray-500 dark:text-gray-400">© 2025 FinanceApp. Все права защищены.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
