<script setup>
import { ref, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import { useLanguageStore } from '@/stores/languageStore'
import Header from '@/components/Header.vue'
import CreateAccountModal from '@/components/Modals/CreateAccountModal.vue'
import CreateTransactionModal from '@/components/Modals/CreateTransactionModal.vue'
import CreateCategoryModal from '@/components/Modals/CreateCategoryModal.vue'
import CreateFriendModal from '@/components/Modals/CreateFriendModal.vue'

// Модальные окна
const showModal = ref(false)
const modalType = ref(null) // account, transaction, category, friend
const editData = ref(null)

function openModal(type, data = null) {
  modalType.value = type
  editData.value = data
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  modalType.value = null
  editData.value = null
}

function onModalSaved() {
  window.dispatchEvent(new CustomEvent('modalSaved', { detail: { type: modalType.value } }))
}

// Глобальный обработчик для открытия модалок из views
function handleOpenModal(event) {
  const { type, data } = event.detail || {}
  if (type) {
    openModal(type, data)
  }
}

window.addEventListener('openModal', handleOpenModal)
onUnmounted(() => {
  window.removeEventListener('openModal', handleOpenModal)
})

const themeStore = useThemeStore()
const languageStore = useLanguageStore()
</script>

<template>
  <div :class="['min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200']">
    <Header @logout="$emit('logout')" />

    <!-- Modal Container -->
    <transition name="fade" mode="out-in">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
        <!-- Account Modal -->
        <CreateAccountModal
          v-if="modalType === 'account'"
          :modelValue="showModal"
          :edit-data="editData"
          @update:modelValue="showModal = $event"
          @saved="closeModal"
        />

        <!-- Transaction Modal -->
        <CreateTransactionModal
          v-else-if="modalType === 'transaction'"
          :modelValue="showModal"
          :edit-data="editData"
          @update:modelValue="showModal = $event"
          @saved="closeModal"
        />

        <!-- Category Modal -->
        <CreateCategoryModal
          v-else-if="modalType === 'category'"
          :modelValue="showModal"
          :edit-data="editData"
          @update:modelValue="showModal = $event"
          @saved="onModalSaved"
        />

        <!-- Friend Modal -->
        <CreateFriendModal
          v-else-if="modalType === 'friend'"
          :modelValue="showModal"
          :edit-data="editData"
          @update:modelValue="showModal = $event"
          @saved="closeModal"
        />
      </div>
    </transition>

    <main class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
