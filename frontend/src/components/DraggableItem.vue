<!--
  Draggable Item Component
  
  Represents individual statement items that can be dragged between factor groups.
  Each item displays the statement text and handles drag operations.
  
  Features:
  - Draggable interface for moving statements between groups
  - Supports both legacy number format and new object format for statements
  - Custom drag image positioning for better UX
  - Tooltip support for long statement text
  - Compact display optimized for factor analysis workflow
  
  Props:
  - item: Statement data (Number for legacy, Object with displayText for new format)
  - groupIndex: Index of the group containing this item
  - itemIndex: Position of this item within its group
-->

<template>
  <li
    class="list-group-item"
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
    :title="item.displayText || `Stelling ${item}`"
  >
    <span class="item-text">
      {{ item.displayText || `Stelling ${item}` }}
    </span>
  </li>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import apiService from '../services/apiService.js';

const props = defineProps({
  item: [Number, Object], // Support both legacy Number format and new Object format
  groupIndex: Number,     // Index of the containing group
  itemIndex: Number       // Position within the group
});

// Events emitted during drag operations
const emit = defineEmits(['dragstart', 'dragend', 'cronbach-calculated']);

/**
 * Handle drag start event
 * Sets up custom drag image and notifies parent components
 */
async function onDragStart() {
  // Customize drag image position for better user experience
  event.dataTransfer.setDragImage(event.target, 100, 20);
  console.log("Drag started - triggering Cronbach's Alpha calculation")
  
  emit('dragstart', props.groupIndex, props.itemIndex);
}

/**
 * Handle drag end event
 * Determines drop target and notifies parent components
 */
async function onDragEnd(event) {
  console.log("Drag ended");
  // Find the drop target by looking for the closest ul element
  const target = event.relatedTarget?.closest('ul');
  console.log("Dropped on target:", target);

  emit('dragend', props.groupIndex, props.itemIndex, target);
}



</script>

<style scoped>
.list-group-item {
  cursor: grab;
  display: flex;
  text-align: center;
  align-items: center;
  margin-bottom: 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
  height: 25px;
  position: relative;
  padding: 0 8px;
  overflow: hidden;
}

.item-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  text-align: center;
}

.list-group-item:active {
  cursor: grabbing;
}
</style>