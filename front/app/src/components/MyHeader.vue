<script setup>
  import { Bars3Icon } from '@heroicons/vue/24/solid'
  
  defineProps({
    currentTab: {
      type: String,
      required: true,
    },
    userName: {
      type: String,
      required: true,
    },
    showMenuButton: {
      type: Boolean,
      default: false,
    }
  })

  const emit = defineEmits(['menuClick'])

  const handleMenuClick = () => {
    emit('menuClick')
  }
</script>


<template>
  <div class="flex justify-between items-center mb-6 lg:mb-8 px-4">
    <!-- Mobile Menu Button -->
    <button 
      v-if="showMenuButton"
      @click="handleMenuClick"
      class="lg:hidden p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
      aria-label="Open menu"
    >
      <Bars3Icon class="w-6 h-6 text-gray-700 dark:text-gray-300" />
    </button>

    <!-- Page Title (centered on mobile) -->
    <h1 :class="[
      'text-xl lg:text-2xl font-bold capitalize',
      showMenuButton ? '' : 'text-left'
    ]">{{ currentTab }}</h1>

    <!-- Right side actions -->
    <div class="flex items-center gap-3">
      <!-- Search button (hidden on small screens) -->
      <button 
        v-if="!showMenuButton"
        class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 hidden md:block transition-colors"
        aria-label="Search"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>

      <!-- Notifications (hidden on small screens) -->
      <button 
        class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 hidden md:block transition-colors relative"
        aria-label="Notifications"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
      </button>

      <!-- User avatar -->
      <div class="flex items-center gap-2 pl-2">
        <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-semibold text-sm md:text-base shadow-md">
          {{ userName.charAt(0).toUpperCase() }}
        </div>
        <span v-if="!showMenuButton" class="hidden sm:block font-medium text-gray-700 dark:text-gray-300">{{userName}}</span>
      </div>

    </div>
  </div>
</template>

<style scoped>
  .dark svg {
    color: #9ca3af;
  }
  .dark button:hover {
    background-color: #374151;
  }
</style>
