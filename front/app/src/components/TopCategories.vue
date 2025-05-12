<script setup lang="ts">
  import { ref } from 'vue'
  import { EllipsisHorizontalIcon, PlusIcon } from '@heroicons/vue/24/outline'

  const emit = defineEmits([
        'addCategory', 'deleteCategory'
        ])

  const props = defineProps<{
    categories: any[]
  }>()

  const showNewCategoryModal = ref(false)
  const showDropdown = ref<number | null>(null)
  const newCategoryName = ref('')
  const newCategoryType = ref('expense')

  const toggleDropdown = (categoryId: number) => {
    showDropdown.value = showDropdown.value === categoryId ? null : categoryId
  }

  const handleClickOutside = (event: Event) => {
    const target = event.target as HTMLElement
    if (!target.closest('.dropdown-menu') && !target.closest('.dropdown-trigger')) {
      showDropdown.value = null
    }
  }

  const openNewCategoryModal = () => {
    showNewCategoryModal.value = true
    newCategoryName.value = ''
    newCategoryType.value = 'expense'
  }

  const createNewCategory = () => {
    if (newCategoryName.value) {
      const newCategory = {
        id: Date.now(),
        name: newCategoryName.value,
        amount: 0.00,
        percentage: '0%',
        type: newCategoryType.value
      }
      emit('addCategory', newCategory)
      showNewCategoryModal.value = false
    }
  }

  const deleteCategory = (categoryId: number, categoryType: string) => {
    emit('deleteCategory', {categoryId, categoryType})
    showDropdown.value = null
  }

  const debitCategory = () => {
    return props.categories.filter(categ => categ.typeCategory === 'Debit')
  }

  const creditCategory = () => {
    return props.categories.filter(categ => categ.typeCategory === 'Credit')
  }
</script>

<template>
  <div class="bg-white rounded-xl p-4">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg font-bold">Categories</h2>
      <button
        @click="openNewCategoryModal"
        class="flex items-center gap-2 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
      >
        <PlusIcon class="w-5 h-5" />
        <span>Category</span>
      </button>
    </div>

    <!-- Expense Categories -->
    <div class="mb-8">
      <h3 class="text-md font-semibold mb-4 text-gray-700">Expense Categories</h3>
      <div class="space-y-3">
        <div
          v-for="category in debitCategory()"
          :key="category.id"
          class="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg relative"
        >
          <div>
            <div class="font-medium">{{ category.name }}</div>
            <!-- <div class="text-sm text-gray-500">${{ category.amount.toLocaleString() }}</div> -->
          </div>
          <div class="flex items-center gap-3">
            <!-- <div class="text-sm text-gray-600">{{ category.percentage }}</div> -->
            <button
              class="dropdown-trigger p-1 hover:bg-gray-100 rounded-full"
              @click="toggleDropdown(category.id)"
            >
              <EllipsisHorizontalIcon class="w-5 h-5 text-gray-500" />
            </button>
            <div
              v-if="showDropdown === category.id"
              class="dropdown-menu absolute right-0 top-12 bg-white shadow-lg rounded-lg py-1 min-w-[120px] z-10"
            >
              <button
                class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
                @click="() => {}"
              >
                Edit
              </button>
              <button
                class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm text-red-600"
                @click="deleteCategory(category.id, 'expense')"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Income Categories -->
    <div>
      <h3 class="text-md font-semibold mb-4 text-gray-700">Income Categories</h3>
      <div class="space-y-3">
        <div
          v-for="category in creditCategory()"
          :key="category.id"
          class="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg relative"
        >
          <div>
            <div class="font-medium">{{ category.name }}</div>
            <!-- <div class="text-sm text-gray-500">${{ category.amount.toLocaleString() }}</div> -->
          </div>
          <div class="flex items-center gap-3">
            <!-- <div class="text-sm text-gray-600">{{ category.percentage }}</div> -->
            <button
              class="dropdown-trigger p-1 hover:bg-gray-100 rounded-full"
              @click="toggleDropdown(category.id)"
            >
              <EllipsisHorizontalIcon class="w-5 h-5 text-gray-500" />
            </button>
            <div
              v-if="showDropdown === category.id"
              class="dropdown-menu absolute right-0 top-12 bg-white shadow-lg rounded-lg py-1 min-w-[120px] z-10"
            >
              <button
                class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
                @click="() => {}"
              >
                Edit
              </button>
              <button
                class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm text-red-600"
                @click="deleteCategory(category.id, 'income')"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New Category Modal -->
    <div v-if="showNewCategoryModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Create New Category</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category Name</label>
            <input
              v-model="newCategoryName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Enter category name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category Type</label>
            <select
              v-model="newCategoryType"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="showNewCategoryModal = false"
            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            @click="createNewCategory"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Create Category
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dropdown-menu {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
</style>
