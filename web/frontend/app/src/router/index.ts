import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import Login from '../views/LoginView.vue'
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
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/project/create',
      name: 'create-project',
      component: () => import('../views/CreateProjectView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/project/:id/risk-discovery',
      name: 'risk-discovery',
      component: () => import('../views/RiskDiscoveryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/project/:id/qualitative-analysis',
      name: 'qualitative-analysis',
      component: () => import('../views/QualitativeAnalysisView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/project/:id/planning',
      name: 'planning',
      component: () => import('../views/PlanningView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/project/:id/overview',
      name: 'project-overview',
      component: () => import('../views/ProjectOverviewView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/oops',
      name: 'oops',
      component: () => import('../views/OopsView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
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
