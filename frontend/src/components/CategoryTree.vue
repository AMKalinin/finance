<script setup>
import { ref } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    required: true
  },
  level: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['edit', 'delete'])

// Храним состояние раскрытия для каждой категории
const expanded = ref({})

function toggleExpand(id) {
  expanded.value[id] = !expanded.value[id]
}

function isExpanded(id) {
  return expanded.value[id] ?? false
}

function getCategoryColor(type) {
  switch (type) {
    case 'expense': return 'text-red-600'
    case 'income': return 'text-green-600'
    case 'transfer': return 'text-blue-600'
    default: return 'text-gray-700 dark:text-gray-300'
  }
}

function getPaddingClass(level) {
  return 'pl-' + (6 + level * 4)
}

function getIndentLine(level) {
  if (level <= 0) return ''
  return '│&nbsp;&nbsp;&nbsp;'.repeat(level - 1) + '├&nbsp;'
}

function hasChildren(category) {
  const children = category.subCategory || category.children || []
  return children.length > 0
}
</script>

<template>
  <ul class="space-y-0.5">
    <li
      v-for="category in categories"
      :key="category.id"
      class="group"
    >
      <!-- Category row -->
      <div
        class="flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors hover:bg-gray-100 dark:hover:bg-gray-700"
        :class="[getPaddingClass(level), { 'font-semibold': level === 0 }]"
        @click="emit('edit', category)"
      >
        <div class="flex items-center gap-2">
          <!-- Expand/collapse toggle -->
          <button
            v-if="hasChildren(category)"
            @click.stop="toggleExpand(category.id)"
            class="w-5 h-5 flex items-center justify-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <svg
              class="w-4 h-4 transform transition-transform duration-200"
              :class="{ 'rotate-90': isExpanded(category.id) }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <span v-else class="w-5" />

          <!-- Icon -->
          <span
            class="text-xl w-6 text-center"
            :class="getCategoryColor(category.type)"
          >
            {{ category.icon || '📁' }}
          </span>
          <!-- Name -->
          <span
            class="text-gray-900 dark:text-gray-100"
          >
            {{ category.name }}
          </span>
          <!-- Children count badge -->
          <span
            v-if="hasChildren(category)"
            class="text-xs bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 px-1.5 py-0.5 rounded-full"
          >
            {{ category.subCategory?.length || category.children?.length || 0 }}
          </span>
        </div>

        <!-- Delete button -->
        <button
          @click.stop="emit('delete', category.id, category.name)"
          class="opacity-0 group-hover:opacity-100 p-1.5 bg-red-50 dark:bg-red-900/30 hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 rounded transition-colors"
        >
          🗑️
        </button>
      </div>

      <!-- Children recursively -->
      <ul
        v-if="hasChildren(category) && isExpanded(category.id)"
        class="space-y-0.5 border-l-2 border-gray-200 dark:border-gray-700 ml-3"
      >
        <CategoryTree
          :categories="category.subCategory || category.children"
          :level="level + 1"
          @edit="(cat) => emit('edit', cat)"
          @delete="(id, name) => emit('delete', id, name)"
        />
      </ul>
    </li>
  </ul>
</template>

<style scoped>
ul {
  list-style: none;
}
</style>
