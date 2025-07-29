<!--
  Table Footer Component
  
  Displays the Cronbach's alpha reliability score for each factor group.
  Features:
  - Color-coded scoring system for easy interpretation
  - Formatted to 3 decimal places for precision
  - Red: < 0.7 (poor reliability)
  - Orange: 0.7-0.89 (acceptable reliability)
  - Green: ≥ 0.9 (excellent reliability)
  
  Props:
  - groupScore: Cronbach's alpha value (0-1) or null if not calculated
-->

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

// Format the score for display with appropriate precision
const displayScore = computed(() => {
  if (props.groupScore === null || props.groupScore === undefined) {
    return 'N/A';
  }
  return props.groupScore.toFixed(3);
});

// Color-code the score based on reliability thresholds
const scoreColor = computed(() => {
  if (props.groupScore === null || props.groupScore === undefined) {
    return 'inherit'; // Default color for N/A
  }
  
  // Cronbach's alpha interpretation scale
  if (props.groupScore < 0.7) {
    return '#ff0000'; // Red for poor reliability (< 0.7)
  } else if (props.groupScore < 0.9) {
    return '#ffb600'; // Orange for acceptable reliability (0.7-0.89)
  } else {
    return '#009902'; // Green for excellent reliability (≥ 0.9)
  }
});
</script>

<style scoped>
.table-footer {
  margin-top: 0.5rem;
  font-style: italic;
}
</style>