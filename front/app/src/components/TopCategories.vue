<script setup lang="ts">
  import { ref, computed, watch } from 'vue'
  import { PlusIcon, TrashIcon } from '@heroicons/vue/24/outline'

  interface Props {
    categories: any[]
  }

  const props = withDefaults(defineProps<Props>(), {
    categories: () => []
  })

  const emit = defineEmits(['addCategory', 'deleteCategory'])

  const showNewCategoryModal = ref(false)
  const newCategoryName = ref('')
  const newCategoryType = ref<'Debit' | 'Credit'>('Debit')

  const openNewCategoryModal = () => {
    showNewCategoryModal.value = true
    newCategoryName.value = ''
    newCategoryType.value = 'Debit'
  }

  const createNewCategory = () => {
    if (newCategoryName.value) {
      emit('addCategory', {
        name: newCategoryName.value,
        type: newCategoryType.value
      })
      showNewCategoryModal.value = false
    }
  }

  const deleteCategory = (categoryId: string) => {
    emit('deleteCategory', categoryId)
  }

  // Разделяем категории на расходы и доходы
  const expenseCategories = computed(() => {
    if (!props.categories) return []
    return props.categories.filter((cat: any) => cat.type === 'Debit' || (Array.isArray(cat.subCategory) && cat.subCategory.some((sub: any) => sub.type === 'Debit')))
      .sort((a, b) => a.name.localeCompare(b.name))
  })

  const incomeCategories = computed(() => {
    if (!props.categories) return []
    return props.categories.filter((cat: any) => cat.type === 'Credit' || (Array.isArray(cat.subCategory) && cat.subCategory.some((sub: any) => sub.type === 'Credit')))
      .sort((a, b) => a.name.localeCompare(b.name))
  })

  const totalCategories = computed(() => {
    return props.categories?.length || 0
  })
</script>


<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden">
    
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 p-4 border-b dark:border-gray-700">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white">Top Categories</h2>
      <button
        @click="openNewCategoryModal"
        class="flex items-center gap-2 px-3 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150"
      >
        <PlusIcon class="w-5 h-5" />
        <span class="hidden sm:inline">Category</span>
      </button>
    </div>

    <!-- Category List -->
    <div class="p-4 space-y-3 max-h-[calc(100vh-200px)] overflow-y-auto">
      
      <div v-if="totalCategories > 0" class="flex justify-between items-center mb-2 px-1">
        <p class="text-xs text-gray-500 dark:text-gray-400">Total Categories</p>
        <p class="text-sm font-bold text-gray-900 dark:text-white">{{ totalCategories }}</p>
      </div>

      <!-- Expenses Section -->
      <div v-if="expenseCategories.length > 0">
        <h3 class="text-xs font-semibold text-red-600 dark:text-red-400 uppercase tracking-wide mb-2 px-1">Expenses</h3>
        <div class="space-y-2">
          <div
            v-for="(category, index) in expenseCategories.slice(0, 5)" 
            :key="category.id"
            @click="deleteCategory(String(category.id))"
            class="w-full flex items-center justify-between p-3 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors group text-left cursor-pointer"
          >
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <!-- Icon -->
              <div class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/40 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600 dark:text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              
              <span class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ category.name }}</span>
            </div>

            <!-- Delete Button (visible on hover) -->
            <button 
              @click.stop="deleteCategory(String(category.id))"
              class="opacity-0 group-hover:opacity-100 p-2 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/40 rounded-lg transition-all duration-200 flex-shrink-0 ml-2"
              title="Delete category"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Income Section -->
      <div v-if="incomeCategories.length > 0">
        <h3 class="text-xs font-semibold text-green-600 dark:text-green-400 uppercase tracking-wide mb-2 px-1 mt-4">Income</h3>
        <div class="space-y-2">
          <div
            v-for="(category, index) in incomeCategories.slice(0, 5)" 
            :key="category.id"
            @click="deleteCategory(String(category.id))"
            class="w-full flex items-center justify-between p-3 rounded-lg hover:bg-green-50 dark:hover:bg-green-900/20 transition-colors group text-left cursor-pointer"
          >
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <!-- Icon -->
              <div class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/40 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              
              <span class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ category.name }}</span>
            </div>

            <!-- Delete Button (visible on hover) -->
            <button 
              @click.stop="deleteCategory(String(category.id))"
              class="opacity-0 group-hover:opacity-100 p-2 text-green-600 hover:bg-green-100 dark:hover:bg-green-900/40 rounded-lg transition-all duration-200 flex-shrink-0 ml-2"
              title="Delete category"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="totalCategories === 0" class="text-center py-8 px-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 opacity-50 text-gray-400 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        <p class="text-sm text-gray-500 dark:text-gray-400">No categories yet</p>
      </div>

    </div>
  </div>

  <!-- New Category Modal -->
  <div v-if="showNewCategoryModal" class="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md">
      <h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Create New Category</h3>
      
      <div class="space-y-4">
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category Name</label>
          <input
            v-model="newCategoryName"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="e.g., Groceries"
          />
        </div>

        <!-- Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category Type</label>
          <select
            v-model="newCategoryType"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="Debit">Expense (Расход)</option>
            <option value="Credit">Income (Доход)</option>
          </select>
        </div>

        <!-- Visual indicator -->
        <div class="flex items-center gap-3 pt-2">
          <div :class="[
            'w-10 h-10 rounded-lg flex items-center justify-center transition-colors',
            newCategoryType === 'Debit' ? 'bg-red-100 dark:bg-red-900/40' : 'bg-green-100 dark:bg-green-900/40'
          ]">
            <svg v-if="newCategoryType === 'Debit'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600 dark:text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </div>
          <span :class="[
            'text-sm',
            newCategoryType === 'Debit' ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'
          ]">
            {{ newCategoryType === 'Debit' ? 'Expense (Расход)' : 'Income (Доход)' }}
          </span>
        </div>
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <button
          @click="showNewCategoryModal = false"
          class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          Cancel
        </button>
        <button
          @click="createNewCategory"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors shadow-sm active:scale-95 transform duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!newCategoryName"
        >
          Create Category
        </button>
      </div>
    </div>
  </div>

</template>

<style scoped>
/* Smooth transitions */
.group:hover .opacity-0 {
  opacity: 1 !important;
}

/* Custom scrollbar for category list */
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
::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}

.dark ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
}
</style>
