<template>
  <div class="database-combiner-page">
    <h1>Database Combiner</h1>
    <DatabaseCombiner />
  </div>
</template>

<script setup>
import DatabaseCombiner from '../components/DatabaseCombiner.vue';
</script>

<style scoped>
.database-combiner-page {
  min-height: 100vh;
  padding: 2rem;
}

.database-combiner-page h1 {
  margin-bottom: 2rem;
  color: var(--color-heading);
  text-align: center;
}

@media (min-width: 1024px) {
  .database-combiner-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 800px;
    margin: 0 auto;
  }
}
</style>
