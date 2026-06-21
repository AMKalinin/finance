import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { defineStore } from 'pinia'

export const useLanguageStore = defineStore('language', () => {
  const { locale, t } = useI18n()
  
  const currentLocale = ref(localStorage.getItem('locale') || 'ru')

  watch(currentLocale, (newLocale) => {
    locale.value = newLocale
    localStorage.setItem('locale', newLocale)
  })

  function setLanguage(lang) {
    if (['en', 'ru'].includes(lang)) {
      currentLocale.value = lang
    }
  }

  function toggleLanguage() {
    setLanguage(currentLocale.value === 'ru' ? 'en' : 'ru')
  }

  return {
    currentLocale,
    t,
    setLanguage,
    toggleLanguage,
  }
})
