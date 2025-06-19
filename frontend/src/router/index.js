  	import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import FactorCalculator from '@/pages/FactorCalculator.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'UploadPage',
      component: () => import('@/pages/UploadPage.vue'),
    },
    {
      path: '/FactorCalculator',
      name: 'FactorCalculator',
      component: () => import('@/pages/FactorCalculator.vue'),
    },
    {
      path: '/download',
      name: 'download',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/pages/DownloadPage.vue'),
    },
  ],
  
})

export default router
