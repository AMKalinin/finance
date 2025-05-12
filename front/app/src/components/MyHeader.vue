<script setup>
  defineProps({
    currentTab: {
      type: String,
      required: true,
    },
    userName: {
      type: String,
      required: true,
    },
  })
</script>


<template>

  <div class="flex justify-between items-center mb-8">
    <h1 class="text-2xl font-bold capitalize">{{ currentTab }}</h1>
    <div class="flex items-center gap-4">

      <button class="p-2 rounded-full hover:bg-gray-200 opacity-0">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>

      <button class="p-2 rounded-full hover:bg-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
      </button>

      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-gray-300 rounded-full"></div>
        <span class="font-medium">{{userName}}</span>
      </div>

    </div>
  </div>
</template>
