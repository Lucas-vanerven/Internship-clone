<template>
  <button class="btn btn-primary" @click="handleClick" :disabled="loading">
    <!-- <span>{{ loading ? 'Opslaan...' : 'Opslaan' }}</span> -->
    <span style="color: white;">{{ loading ? 'Opslaan...' : 'Opslaan' }}</span>
  </button>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['click']);
const loading = ref(false);

async function handleClick() {
  loading.value = true;
  try {
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