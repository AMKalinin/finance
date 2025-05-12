<script setup lang="ts">
  import TransactionTable from '@/components/TransactionTable.vue'

  const emit = defineEmits(['addTransaction', 'deleteTransaction'])

  const props = defineProps<{
    transactions: any[]
  }>()

</script>

<template>

  <div class="bg-white p-6 rounded-xl">
    <TransactionTable
      :transactions="transactions"
      @add-transaction="emit('addTransaction', $event)"
      @delete-transaction="emit('deleteTransaction', $event)"
    />
  </div>

</template>

