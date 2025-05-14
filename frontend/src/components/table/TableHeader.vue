<template>
  <div class="table-header text-center">
    Groep {{ groupIndex + 1 }}
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  groupIndex: Number
});
</script>

<style scoped>
.table-header {
  font-weight: bold;
  margin-bottom: 0.5rem;
}
</style>