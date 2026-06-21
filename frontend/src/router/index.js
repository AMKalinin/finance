import { createRouter, createWebHistory } from 'vue-router'
import { getToken, isUserAuthenticated } from '@/keycloak/keycloak-init'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/accounts',
    name: 'Accounts',
    component: () => import('@/views/AccountsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: () => import('@/views/TransactionsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/categories',
    name: 'Categories',
    component: () => import('@/views/CategoriesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/friends',
    name: 'Friends',
    component: () => import('@/views/FriendsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = isUserAuthenticated()
  const token = await getToken()

  if (to.meta.requiresAuth && (!isAuthenticated || !token)) {
    next('/login')
  } else if (to.meta.guestOnly && isAuthenticated && token) {
    next('/')
  } else {
    next()
  }
})

export default router
