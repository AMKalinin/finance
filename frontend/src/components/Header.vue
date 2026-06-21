<script setup>
import { computed, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/stores/themeStore'
import { useLanguageStore } from '@/stores/languageStore'
import { useRouter } from 'vue-router'

const { t } = useI18n()

const emit = defineEmits(['logout'])

const router = useRouter()
const themeStore = useThemeStore()
const languageStore = useLanguageStore()

function navigateTo(pageName) {
  if (pageName && router.currentRoute.value.name !== pageName) {
    router.push({ name: pageName })
  }
}

function toggleThemeMode() {
  const modes = ['light', 'dark', 'auto']
  const currentIndex = modes.indexOf(themeStore.themeMode)
  themeStore.setThemeMode(modes[(currentIndex + 1) % modes.length])
}

const themeIcon = computed(() => {
  if (themeStore.isDark.value) return '🌙'
  return '☀️'
})

// Detect mobile viewport
const isMobile = ref(window.innerWidth < 640)

onMounted(() => {
  const handleResize = () => {
    isMobile.value = window.innerWidth < 640
  }
  
  window.addEventListener('resize', handleResize)
  
  // Cleanup on unmount
  return () => {
    window.removeEventListener('resize', handleResize)
  }
})

// Navigation items with icons and labels for desktop, only icons for mobile
const navItems = [
  { name: 'Dashboard', icon: '📊', labelKey: 'nav.dashboard' },
  { name: 'Accounts', icon: '💰', labelKey: 'nav.accounts' },
  { name: 'Transactions', icon: '📋', labelKey: 'nav.transactions' },
  { name: 'Categories', icon: '📁', labelKey: 'nav.categories' },
  { name: 'Friends', icon: '👥', labelKey: 'nav.friends' }
]

// Action items for desktop (top header) and mobile (bottom nav)
const actionItems = [
  { type: 'search', icon: '🔍', title: 'Search' },
  { type: 'notifications', icon: '🔔', hasBadge: true, title: 'Notifications' },
  { type: 'theme', icon: computed(() => themeIcon), onClick: toggleThemeMode, title: themeStore.isDark ? 'Switch to light theme' : 'Switch to dark theme' },
  { type: 'language', icon: computed(() => languageStore.currentLocale === 'ru' ? 'RU' : 'EN'), onClick: () => languageStore.toggleLanguage(), style: "color: #2563EB;", title: 'Switch to ' + (languageStore.currentLocale === 'ru' ? 'English' : 'Русский') },
  { type: 'avatar', text: 'АК', class: 'bg-blue-600 dark:bg-blue-500 text-white' },
  { type: 'logout', icon: '🔒', onClick: () => $emit('logout'), title: 'Logout', styleClass: 'text-red-500 hover:bg-red-50' }
]
</script>

<template>
  <!-- Desktop Header (top) - visible on >= sm screens -->
  <header v-show="!isMobile" class="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Logo -->
      <a href="#" @click.prevent="navigateTo('Dashboard')" class="flex items-center gap-2 text-blue-600 dark:text-blue-400 font-bold text-lg hover:opacity-80 transition-opacity">
        <div class="w-9 h-9 bg-blue-600 dark:bg-blue-500 rounded-md flex items-center justify-center text-white font-bold">₿</div>
        <span class="hidden sm:inline">FinanceApp</span>
      </a>

      <!-- Navigation -->
      <nav class="flex items-center gap-1 overflow-x-auto scrollbar-hide">
        <button 
          v-for="item in navItems" 
          :key="item.name"
          @click="navigateTo(item.name)" 
          :class="[
            'px-3 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
            router.currentRoute.value.name === item.name
              ? 'bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]">
          {{ item.icon }} {{ t(item.labelKey) }}
        </button>
      </nav>

      <!-- Actions -->
      <div class="flex items-center gap-2">
        <!-- Search -->
        <button 
          v-for="item in actionItems.filter(i => i.type === 'search' || i.type === 'notifications')" 
          :key="item.type"
          :class="[
            'w-9 h-9 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors',
            item.type === 'notifications' ? 'relative' : ''
          ]" 
          :title="item.title">
          {{ item.icon }}
          <span v-if="item.hasBadge && Math.random() > 0.5" class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <!-- Theme Toggle -->
        <button 
          @click="toggleThemeMode()" 
          :title="themeStore.isDark ? 'Switch to light theme' : 'Switch to dark theme'" 
          class="w-9 h-9 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 flex items-center justify-center text-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
          {{ themeIcon }}
        </button>

        <!-- Language Toggle -->
        <button 
          @click="languageStore.toggleLanguage()" 
          :title="'Switch to ' + (languageStore.currentLocale === 'ru' ? 'English' : 'Русский')" 
          class="w-9 h-9 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 flex items-center justify-center text-sm font-bold hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
          style="color: #2563EB;">
          {{ languageStore.currentLocale === 'ru' ? 'RU' : 'EN' }}
        </button>

        <!-- User Avatar -->
        <div class="w-9 h-9 rounded-full bg-blue-600 dark:bg-blue-500 text-white flex items-center justify-center font-bold text-sm cursor-pointer hover:ring-2 ring-blue-100 transition-ring">
          АК
        </div>

        <!-- Logout -->
        <button 
          @click="$emit('logout')" 
          class="w-9 h-9 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 flex items-center justify-center text-red-500 hover:bg-red-50 transition-colors"
          title="Logout">
          🔒
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Bottom Navigation - visible on < sm screens -->
  <nav v-show="isMobile" class="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 transition-colors duration-200">
    <!-- Logo bar (small) -->
    <div class="px-4 py-2 flex items-center justify-between">
      <a href="#" @click.prevent="navigateTo('Dashboard')" class="flex items-center gap-2 text-blue-600 dark:text-blue-400 font-bold">
        <div class="w-8 h-8 bg-blue-600 dark:bg-blue-500 rounded-md flex items-center justify-center text-white font-bold text-base">₿</div>
      </a>
    </div>
    
    <!-- Navigation icons only (no labels) -->
    <div class="flex items-center justify-around py-2">
      <button 
        v-for="item in navItems" 
        :key="item.name"
        @click="navigateTo(item.name)"
        :class="[
          'w-14 h-14 rounded-xl flex items-center justify-center text-2xl transition-colors',
          router.currentRoute.value.name === item.name
            ? 'bg-blue-50 dark:bg-blue-900/50'
            : 'hover:bg-gray-100 dark:hover:bg-gray-700'
        ]">
        {{ item.icon }}
      </button>
    </div>

    <!-- Action icons bar -->
    <div class="flex items-center justify-around py-2 border-t border-gray-200 dark:border-gray-700 mt-1 pt-2">
      <!-- Search -->
      <button 
        :class="[
          'w-14 h-14 rounded-xl flex items-center justify-center text-2xl transition-colors',
          router.currentRoute.value.name ? 'hover:bg-gray-100 dark:hover:bg-gray-700' : ''
        ]"
        title="Search">
        🔍
      </button>

      <!-- Notifications -->
      <button 
        class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl transition-colors relative hover:bg-gray-100 dark:hover:bg-gray-700"
        title="Notifications">
        🔔
        <span v-if="Math.random() > 0.5" class="absolute top-3 right-4 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>

      <!-- Theme Toggle -->
      <button 
        @click="toggleThemeMode()"
        :title="themeStore.isDark ? 'Switch to light theme' : 'Switch to dark theme'"
        class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl transition-colors hover:bg-gray-100 dark:hover:bg-gray-700">
        {{ themeIcon }}
      </button>

      <!-- Language Toggle -->
      <button 
        @click="languageStore.toggleLanguage()"
        :title="'Switch to ' + (languageStore.currentLocale === 'ru' ? 'English' : 'Русский')"
        class="w-14 h-14 rounded-xl flex items-center justify-center text-sm font-bold transition-colors hover:bg-gray-100 dark:hover:bg-gray-700"
        style="color: #2563EB;">
        {{ languageStore.currentLocale === 'ru' ? 'RU' : 'EN' }}
      </button>

      <!-- User Avatar -->
      <div class="w-14 h-14 rounded-xl bg-blue-600 dark:bg-blue-500 text-white flex items-center justify-center font-bold text-lg cursor-pointer hover:ring-2 ring-blue-100 transition-ring">
        АК
      </div>

      <!-- Logout -->
      <button 
        @click="$emit('logout')"
        class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl text-red-500 hover:bg-red-50 transition-colors"
        title="Logout">
        🔒
      </button>
    </div>

    <!-- Safe area for notched devices -->
    <div class="h-safe-area-bottom"></div>
  </nav>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Safe area for notched devices (iPhone X and newer) */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .h-safe-area-bottom {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>
