<!--
  Group Card Component
  
  Represents a single factor group in the factor analysis interface.
  Each card contains:
  - Header with group identification and controls
  - Body with draggable statement items
  - Footer displaying Cronbach's alpha reliability score
  
  This component acts as a container that coordinates between:
  - TableHeader: Group title and management controls
  - TableBody: Statement list with drag-and-drop functionality  
  - TableFooter: Reliability score display
  
  Props:
  - group: Array of statement objects in this group
  - groupIndex: Numeric identifier for this group (0-3)
  - groupScore: Cronbach's alpha score for this group
-->

<template>
  <div class="card">
    <!-- Group header with title and controls -->
    <TableHeader :groupIndex="groupIndex" />
    <!-- <v-divider class="border-opacity-100" inset/> --> 
    <div class="card-body">
      <!-- Main content area with statement list -->
      <TableBody :group="group" :groupIndex="groupIndex" @dragstart="onDragStart" @drop="onDrop" />
    </div>
    <!-- Footer showing reliability score -->
    <TableFooter :groupScore="groupScore" />
  </div>
</template>

<script setup>
import TableHeader from './table/TableHeader.vue';
import TableBody from './table/TableBody.vue';
import TableFooter from './table/TableFooter.vue';
import { defineProps, defineEmits } from 'vue';

// Component props for data binding
const props = defineProps({
  group: Array,       // Array of statement objects in this group
  groupIndex: Number, // Index identifier for this group (0-3)
  groupScore: Number  // Cronbach's alpha reliability score
});

// Events emitted to parent for drag-and-drop coordination
const emit = defineEmits(['dragstart', 'drop', 'score-updated']);

/**
 * Handle drag start event - propagate to parent with group context
 */
function onDragStart(groupIndex, itemIndex) {
  emit('dragstart', groupIndex, itemIndex);
}

/**
 * Handle drop event - notify parent that item was dropped in this group
 */
function onDrop() {
  emit('drop', props.groupIndex);
}
</script>

<style scoped>
.card {
  margin-bottom: 0.5rem;
  height: 70vh;
}
.card-body {
  padding: 0;
  overflow-y: auto;
  height: 100%;
}
</style>