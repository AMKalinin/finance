<script setup lang="ts">
  import { ref } from 'vue'
  import TopAccounts from '@/components/TopAccounts.vue'

  const emit = defineEmits(['addAccount', 'deleteAccount'])

  const props = defineProps<{
    accounts: any[]
  }>()
</script>


<template>

  <div class="bg-white p-6 rounded-xl">
    <TopAccounts
      :accounts="accounts"
      @add-account="$emit('addAccount', $event)"
      @delete-account="$emit('deleteAccount', $event)"
    />
  </div>

</template>

