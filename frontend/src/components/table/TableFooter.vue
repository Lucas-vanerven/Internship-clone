<template>
  <div class="table-footer text-center">
    Score: <span :style="{ color: scoreColor }">{{ displayScore }}</span>
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

const scoreColor = computed(() => {
  if (props.groupScore === null || props.groupScore === undefined) {
    return 'inherit'; // Default color for N/A
  }
  
  if (props.groupScore < 0.7) {
    return '#ff0000'; // Red for scores below 0.7
  } else if (props.groupScore < 0.9) {
    return '#ffb600'; // Orange for scores below 0.9
  } else {
    return '#009902'; // Green for scores 0.9 or higher
  }
});
</script>

<style scoped>
.table-footer {
  margin-top: 0.5rem;
  font-style: italic;
}
</style>