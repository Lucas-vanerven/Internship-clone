<template>
  <div class="new-job">
    <h2>Selecteer een bestand</h2>
    <FormBlock />
  </div>
</template>

<script setup>
import FormBlock from './FormBlock.vue';
</script>

<style scoped>
.new-job {
  margin-bottom: 2rem;
}

.new-job h2 {
  margin-bottom: 1rem;
  color: var(--color-heading);
}
</style>
