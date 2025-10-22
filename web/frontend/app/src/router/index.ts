import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import { useCurrentUser } from '@/composables/useCurrentUser'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/create-project',
      name: 'create-project',
      component: () => import('../views/CreateProjectView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/risk-discovery',
      name: 'risk-discovery',
      component: () => import('../views/RiskDiscoveryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/qualitative-analysis',
      name: 'qualitative-analysis',
      component: () => import('../views/QualitativeAnalysisView.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

const { currentUser, fetchUser, clearUser } = useCurrentUser();

// Navigation guard
router.beforeEach(async (to, from, next) => {
  // Only fetch user if we don't have it yet
  let isAuthenticated = currentUser.value !== null;
  
  if (!isAuthenticated && (to.meta.requiresAuth || to.meta.requiresGuest)) {
    isAuthenticated = await fetchUser();
  }

  // If route requires authentication and user is not authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    clearUser();
    next({ name: 'login' });
  }
  // If route requires guest (not logged in) and user is authenticated
  else if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'dashboard' });
  }
  // Allow navigation
  else {
    next();
  }
});

export default router
