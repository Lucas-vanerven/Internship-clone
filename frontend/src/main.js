/**
 * Main Entry Point for Vue.js Application
 * 
 * This file initializes the Vue.js application and mounts it to the DOM.
 * It sets up the application with:
 * - Global styles
 * - Vue Router for navigation
 * - Main App component
 */

import './assets/main.css' // Global CSS styles

import { createApp } from 'vue'
import App from './App.vue' // Root Vue component
import router from './router' // Vue Router configuration

// Create Vue application instance
const app = createApp(App)

// Install Vue Router plugin for navigation
app.use(router)

// Mount the application to the DOM element with id="app"
app.mount('#app')
