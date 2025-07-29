/**
 * Vue Router Configuration
 * 
 * This file defines the routing configuration for the Vue.js application.
 * It sets up navigation between different pages/views in the application.
 * 
 * Available routes:
 * - / : Upload page (main entry point)
 * - /FactorCalculator : Factor analysis and Cronbach's alpha calculation
 * - /download : Download results page
 * 
 * Uses lazy loading for optimal performance - components are loaded
 * only when their routes are visited.
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import FactorCalculator from '@/pages/FactorCalculator.vue'

const router = createRouter({
  // Use HTML5 history mode for clean URLs (no hash)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Default route - Upload page for data input
      path: '/',
      name: 'UploadPage',
      component: () => import('@/pages/UploadPage.vue'),
    },
    // {
    //   path: '/',
    //   name: 'FactorCalculator',
    //   component: () => import('@/pages/FactorCalculator.vue'),
    // },
    {
      // Factor Calculator - Main analysis interface
      path: '/FactorCalculator',
      name: 'FactorCalculator',
      component: () => import('@/pages/FactorCalculator.vue'),
    },
    
  ],

})

export default router
