<script setup lang="ts">
  import { ref, defineEmits} from 'vue'
  import {
    HomeIcon,
    WalletIcon,
    ChartPieIcon,
    ArrowsRightLeftIcon,
    UserIcon,
    Cog6ToothIcon
  } from '@heroicons/vue/24/outline'

  const emit = defineEmits(['tabChange'])
  const menuItems = [
    { name: 'Overview', icon: HomeIcon, id: 'overview' },
    { name: 'Accounts', icon: WalletIcon, id: 'accounts' },
    { name: 'Categories', icon: ChartPieIcon, id: 'categories' },
    { name: 'Transactions', icon: ArrowsRightLeftIcon, id: 'transactions' },
    { name: 'Profile', icon: UserIcon, id: 'profile' },
    // { name: 'Settings', icon: Cog6ToothIcon, id: 'settings' },
  ]

  const activeTab = ref('overview')
  const handleTabClick = (tabId) => {
    activeTab.value = tabId
    emit('tabChange', tabId)
  }
</script>



<template>
  <div class="bg-sidebar dark:bg-gray-900 w-20 lg:w-64 h-screen flex flex-col items-center lg:items-stretch py-8 gap-8 fixed transition-all duration-300">
    <!-- Logo -->
    <div class="w-12 lg:w-full lg:h-auto bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center lg:p-4 shadow-md hover:shadow-lg transition-shadow">
      <span class="text-black dark:text-purple-400 text-2xl font-bold">$</span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 w-full px-3 space-y-2">
      <button
        v-for="item in menuItems"
        :key="item.id"
        @click="handleTabClick(item.id)"
        :class="[
          'w-full rounded-xl flex items-center gap-4 transition-all duration-200',
          activeTab === item.id 
            ? 'bg-white dark:bg-gray-800 shadow-md' 
            : 'hover:bg-black/10 dark:hover:bg-white/5'
        ]"
      >
        <div 
          class="flex flex-col items-center justify-center p-3 lg:p-2 rounded-lg transition-colors min-w-[64px] lg:min-w-0"
        >
          <component
            :is="item.icon"
            :class="[
              'w-6 h-6',
              activeTab === item.id 
                ? 'text-black dark:text-purple-400' 
                : 'text-gray-400 dark:text-gray-500'
            ]"
          />
          <span
            v-if="false" 
            :class="[
              'text-[10px] lg:hidden',
              activeTab === item.id ? 'text-black dark:text-purple-400' : 'text-gray-400 dark:text-gray-500'
            ]"
          >
            {{ item.name }}
          </span>
        </div>

        <!-- Desktop label -->
        <span
          v-if="true"
          :class="[
            'hidden lg:block text-sm font-medium whitespace-nowrap',
            activeTab === item.id 
              ? 'text-black dark:text-purple-400' 
              : 'text-gray-600 dark:text-gray-400'
          ]"
        >
          {{ item.name }}
        </span>
      </button>
    </nav>

    <!-- Footer (optional) -->
    <div class="w-full px-3">
      <div class="text-xs text-center lg:text-left text-gray-500 dark:text-gray-600 px-4 py-2">
        v1.0.0
      </div>
    </div>
  </div>
</template>

<style scoped>
  /* Custom scrollbar for sidebar */
  ::-webkit-scrollbar {
    width: 4px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 2px;
  }
</style>
