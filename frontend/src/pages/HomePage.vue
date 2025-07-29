<!--
  Home Page Component
  
  A simple landing page that displays a welcome message from the backend API.
  This component demonstrates basic API connectivity and serves as an entry point
  for the application.
  
  Features:
  - Fetches and displays welcome message from backend
  - Basic API connection testing
  - Simple layout for initial user interaction
  
  Note: Contains hardcoded API URL that should be made configurable for portability

  Lucas note: Deleting this file will break the app, so it is not deleted.
-->

<template>
  <div>
    <!-- Display welcome message from backend -->
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    // Reactive reference for the welcome message
    const message = ref("");

    // Fetch welcome message from backend when component mounts
    onMounted(async () => {
      try {
        // Possibly replace with your backend API URL
        const response = await fetch("http://127.0.0.1:8000/");
        const data = await response.json();
        message.value = data.message;
      } catch (error) {
        console.error('Failed to fetch welcome message:', error);
        message.value = 'Welcome to Cronbach\'s Alpha Calculator';
      }
    });

    return { message };
  }
};
</script>
