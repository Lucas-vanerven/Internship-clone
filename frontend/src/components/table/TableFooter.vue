<template>
  <div class="table-footer text-center">
    Score: {{ displayScore }}
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  groupScore: {
    type: Number,
    default: null
  }
});

const displayScore = computed(() => {
  if (props.groupScore === null || props.groupScore === undefined) {
    return 'N/A';
  }
  return props.groupScore.toFixed(3);
});
</script>

<style scoped>
.table-footer {
  margin-top: 0.5rem;
  font-style: italic;
}
</style>