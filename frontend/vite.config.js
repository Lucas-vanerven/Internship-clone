/**
 * Vite Configuration File
 * 
 * This file configures the Vite build tool for the Vue.js frontend application.
 * Vite is a fast build tool that provides dev server, hot module replacement,
 * and optimized production builds.
 * 
 * Key configurations:
 * - Vue.js plugin integration
 * - Development tools setup
 * - Build output customization
 * - Asset path resolution
 */

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  // Plugins configuration
  plugins: [
    vue(), // Vue.js single file component support
    vueDevTools(), // Vue developer tools integration for debugging
  ],
  // Module resolution configuration
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)) // Allow '@' as alias for src directory
    },
  },
  // Build configuration for production
  build: {
    // TODO: CHANGE FOR PORTABILITY - This relative path might break in different environments
    // Consider using process.env.BUILD_OUTPUT_DIR or './dist' for better portability
    outDir: '../frontend/dist', //Output directory to backend folder
    emptyOutDir: true, // Clear the output directory before building
    assetsDir: 'assets', //might have to remove the 'static/' part if it causes issues
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  // TODO: CHANGE FOR PORTABILITY - Base path should be configurable for different deployment environments
  // Consider using: base: process.env.VITE_BASE_PATH || '/cronBach/static/'
  base: '/cronBach/static/', // Base path for the built assets
})


