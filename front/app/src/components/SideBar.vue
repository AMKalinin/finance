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
    { name: 'Settings', icon: Cog6ToothIcon, id: 'settings' },
  ]

  const activeTab = ref('overview')
  const handleTabClick = (tabId) => {
    activeTab.value = tabId
    emit('tabChange', tabId)
  }
</script>



<template>
  <div class="bg-sidebar w-20 h-screen flex flex-col items-center py-8 gap-8 fixed">
    <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center">
      <span class="text-black text-2xl font-bold">$</span>
    </div>
    <div class="flex flex-col gap-4">
      <button
        v-for="item in menuItems"
        :key="item.id"
        :class="[
          'w-12 h-12 rounded-xl flex flex-col items-center justify-center transition-colors group',
          activeTab === item.id ? 'bg-white' : 'hover:bg-gray-800'
        ]"
        @click="handleTabClick(item.id)"
      >
        <component
          :is="item.icon"
          :class="[
            'w-6 h-6 mb-1',
            activeTab === item.id ? 'text-black' : 'text-gray-400 group-hover:text-gray-300'
          ]"
        />
        <span
          :class="[
            'text-[10px]',
            activeTab === item.id ? 'text-black' : 'text-gray-400 group-hover:text-gray-300'
          ]"
        >
          {{ item.name }}
        </span>
      </button>
    </div>
  </div>
</template>

<style>
  .bg-sidebar{
    background-color: #1A1D1F !important;
  }
</style>
