<!--
  Table Body Component
  
  Contains the main content area for each factor group, displaying the list
  of statements that can be dragged and dropped between groups.
  
  Features:
  - Renders a list of draggable statement items
  - Handles drop events when items are moved to this group
  - Provides visual feedback during drag operations
  - Maintains minimum height for empty groups to allow drops
  
  Props:
  - group: Array of statement objects in this group
  - groupIndex: Identifier for this group (used in drag/drop operations)
-->

<template>
  <ul class="list-group" @dragover.prevent @drop="onDrop">
    <DraggableItem
      v-for="(item, itemIndex) in group"
      :key="itemIndex"
      :item="item"
      :groupIndex="groupIndex"
      :itemIndex="itemIndex"
      @dragstart="onDragStart"
    />
  </ul>
</template>

<script setup>
// defineProps is no longer needed as an import in Vue 3.3+
// import { defineProps, defineEmits } from 'vue';
import DraggableItem from '../DraggableItem.vue';

const props = defineProps({
  group: Array,       // Array of statement objects to display
  groupIndex: Number  // Index of this group for drag/drop coordination
});

// Events for drag and drop operations
const emit = defineEmits(['dragstart', 'drop']);

/**
 * Handle drag start event - propagate to parent with context
 */
function onDragStart(groupIndex, itemIndex) {
  emit('dragstart', groupIndex, itemIndex);
}

/**
 * Handle drop event - notify parent that item was dropped here
 */
function onDrop() {
  emit('drop', props.groupIndex);
}
</script>

<style scoped>
.list-group {
  padding: 0;
  list-style: none;
  min-height: 100%;
}


</style>