import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import OverviewTab from '@/views/OverviewTab.vue'
import AccountsTab from '@/views/AccountsTab.vue'
import TransactionsTab from '@/views/TransactionsTab.vue'
import ProfileTab from '@/views/ProfileTab.vue'
import CategoriesTab from '@/views/CategoriesTab.vue'

import { isAuthenticated, updateToken } from '../keycloak/keycloak.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/overview',
      name: 'overview',
      component: OverviewTab,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/accounts',
      name: 'accounts',
      component: AccountsTab,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/categories',
      name: 'categories',
      component: CategoriesTab,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileTab,
      meta: { requiresAuth: true }
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: TransactionsTab,
      props: true,
      meta: { requiresAuth: true }
    },

    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  // Обновляем токен при необходимости
  try {
    await updateToken(5)
  } catch (error) {
    console.error('Failed to refresh token', error)
  }

  // Проверяем, требует ли маршрут авторизации
  if (to.meta.requiresAuth && !isAuthenticated()) {
    // Перенаправляем на страницу входа Keycloak
    const keycloak = getKeycloak()
    keycloak.login({ redirectUri: window.location.origin + to.path })
    return
  }
  next()
})

export default router
