<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserInfo, logout } from '../keycloak/keycloak.js'
import router from '../router/router'

const userInfo = ref<any>(null)
const isLoading = ref(true)

const userLogOut = async () => {
  try {
    await logout()
    router.push('/')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

onMounted(() => {
  try {
    const info = getUserInfo()
    if (info) {
      userInfo.value = info
    }
  } catch (error) {
    console.error('Error loading user info:', error)
  } finally {
    isLoading.value = false
  }
})

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2">Profile</h1>
      <p class="text-gray-600 dark:text-gray-400">Manage your account settings and information</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-sm text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-gray-600 dark:text-gray-400">Loading profile...</p>
    </div>

    <!-- Profile Content -->
    <template v-else-if="userInfo">
      
      <!-- Profile Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden mb-6">
        
        <!-- Avatar Banner -->
        <div class="h-24 bg-gradient-to-r from-purple-500 via-pink-500 to-indigo-500"></div>

        <!-- Profile Info -->
        <div class="px-6 pb-6">
          <!-- Avatar and Name -->
          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-4 -mt-12 mb-6">
            <div class="w-24 h-24 bg-white dark:bg-gray-800 rounded-full p-1 shadow-lg">
              <div class="w-full h-full bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-3xl shadow-md">
                {{ userInfo.email?.charAt(0).toUpperCase() }}
              </div>
            </div>
            
            <div class="flex-1 text-center sm:text-left">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ userInfo.preferred_username || 'User' }}</h2>
              <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ userInfo.email }}</p>
            </div>

            <!-- Logout Button -->
            <button 
              @click="userLogOut"
              class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors shadow-sm active:scale-95 transform duration-150 flex items-center gap-2 mt-3 sm:mt-0"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="hidden sm:inline">Logout</span>
            </button>
          </div>

          <!-- Profile Details -->
          <div class="border-t dark:border-gray-700 pt-6 space-y-4">
            
            <!-- Email -->
            <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400 min-w-[100px]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span class="text-sm font-medium">Email</span>
              </div>
              <p class="text-gray-900 dark:text-white break-all">{{ userInfo.email }}</p>
            </div>

            <!-- Name -->
            <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400 min-w-[100px]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span class="text-sm font-medium">Name</span>
              </div>
              <p class="text-gray-900 dark:text-white">{{ userInfo.preferred_username || 'Not set' }}</p>
            </div>

            <!-- User ID -->
            <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <div class="flex items-center gap-2 text-gray-600 dark:text-gray-400 min-w-[100px]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                <span class="text-sm font-medium">User ID</span>
              </div>
              <code class="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-800 dark:text-gray-300 break-all">{{ userInfo.sub }}</code>
            </div>

          </div>
        </div>
      </div>

      <!-- Account Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- Account Settings -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Settings
          </h3>
          
          <div class="space-y-3">
            <button class="w-full flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-left group">
              <span class="text-sm font-medium text-gray-900 dark:text-white">Account Settings</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-hover:text-primary transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            
            <button class="w-full flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-left group">
              <span class="text-sm font-medium text-gray-900 dark:text-white">Privacy</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-hover:text-primary transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

      </div>

    </template>

    <!-- Error State -->
    <template v-else>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-sm text-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p class="text-lg font-medium text-gray-900 dark:text-white mb-2">Unable to load profile</p>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Please check your connection and try again</p>
        <button 
          @click="location.reload()"
          class="px-4 py-2 bg-primary hover:bg-purple-700 text-white rounded-lg transition-colors"
        >
          Reload Page
        </button>
      </div>
    </template>

  </div>
</template>

<style scoped>
/* Smooth transitions */
.group:hover .group-hover\:text-primary {
  color: #6366f1;
}

/* Custom scrollbar for settings list */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.dark ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
}
</style>
