<script setup lang="ts">
  import TopCategories from '@/components/TopCategories.vue'

  const emit = defineEmits([
        'addCategory', 'deleteCategory'
        ])


  const props = defineProps<{
    categories: any[],
  }>()

</script>



<template>

  <div class="bg-white p-6 rounded-xl">
    <TopCategories
      :categories="categories"
      @add-category="$emit('addCategory', $event)"
      @delete-category="$emit('deleteCategory', $event)"
    />
  </div>

</template>

