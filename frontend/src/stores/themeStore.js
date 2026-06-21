import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const themeMode = ref(localStorage.getItem('theme_mode') || 'light') // light, dark, auto
  
  const isDark = computed(() => {
    if (themeMode.value === 'auto') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return themeMode.value === 'dark'
  })

  function setThemeMode(mode) {
    themeMode.value = mode
    localStorage.setItem('theme_mode', mode)
    
    if (mode === 'auto') {
      updateSystemTheme()
    } else {
      document.documentElement.classList.toggle('dark', mode === 'dark')
    }
  }

  function toggleTheme() {
    setThemeMode(themeMode.value === 'dark' ? 'light' : 'dark')
  }

  function updateSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleChange = (e) => {
      document.documentElement.classList.toggle('dark', e.matches)
    }
    
    handleChange(mediaQuery)
    mediaQuery.addEventListener('change', handleChange)
  }

  // Инициализация при загрузке
  if (themeMode.value === 'auto') {
    updateSystemTheme()
  } else {
    document.documentElement.classList.toggle('dark', themeMode.value === 'dark')
  }

  return {
    themeMode,
    isDark,
    setThemeMode,
    toggleTheme,
  }
})
