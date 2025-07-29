<!--
  Opslaan (Save) Button Component
  
  A reusable save button component with loading state management.
  Features:
  - Displays "Opslaan" (Dutch for "Save") text
  - Shows loading state during save operations ("Opslaan...")
  - Disables interaction while saving to prevent duplicate submissions
  - Emits click events to parent components for handling save logic
  - Auto-resets loading state after operation completes
-->

<template>
  <button class="btn btn-primary" @click="handleClick" :disabled="loading">
    <span style="color: white;">{{ loading ? 'Opslaan...' : 'Opslaan' }}</span>
  </button>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

// Emit click events to parent components
const emit = defineEmits(['click']);
// Reactive loading state for UI feedback
const loading = ref(false);

/**
 * Handle button click with loading state management
 * - Sets loading state to provide user feedback
 * - Emits click event for parent to handle save logic
 * - Automatically resets loading state after operation
 */
async function handleClick() {
  loading.value = true;
  try {
    // Emit the click event for parent component to handle
    emit('click');
  } finally {
    // Reset loading state after a short delay to show feedback
    setTimeout(() => {
      loading.value = false;
    }, 1000);
  }
}
</script>

<style scoped>
/* Add any specific styles for the Opslaan button here */
.btn {
  background-color: rgba(60, 57, 80, 1);
  border-color: rgba(60, 57, 80, 1);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  text-align: center;
}
</style>