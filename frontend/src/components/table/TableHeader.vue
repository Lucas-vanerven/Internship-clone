<!--
  Table Header Component
  
  Displays the header for each factor group in the analysis interface.
  Shows "Groep X" (Dutch for "Group X") where X is the group number (1-4).
  
  Props:
  - groupIndex: Zero-based index that gets converted to 1-based display
-->

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