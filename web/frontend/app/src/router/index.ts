import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/create-project',
      name: 'create-project',
      component: () => import('../views/CreateProjectView.vue'),
    },
    {
      path: '/risk-discovery',
      name: 'risk-discovery',
      component: () => import('../views/RiskDiscoveryView.vue'),
    },
    {
      path: '/qualitative-analysis',
      name: 'qualitative-analysis',
      component: () => import('../views/QualitativeAnalysisView.vue'),
    }
  ],
})

export default router
