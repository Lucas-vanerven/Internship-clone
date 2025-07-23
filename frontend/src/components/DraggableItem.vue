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
  item: [Number, Object], // Allow both Number (legacy) and Object (new statement data)
  groupIndex: Number,
  itemIndex: Number
});

const emit = defineEmits(['dragstart', 'dragend', 'cronbach-calculated']);

async function onDragStart() {
  event.dataTransfer.setDragImage(event.target, 100, 20); //offset the drag image from the cursor
  console.log("Drag started - triggering Cronbach's Alpha calculation")
  
  // Example: Call cronbach_alpha function when drag starts
  // In a real scenario, you'd want to collect actual data
  await callCronbachAlpha();
  
  emit('dragstart', props.groupIndex, props.itemIndex);
}

async function onDragEnd(event) {
  console.log("Drag ended");
  const target = event.relatedTarget?.closest('ul'); // Use relatedTarget to get the drop target
  console.log("Dropped on target:", target);
  
  // Call cronbach_alpha again after item is moved
  await callCronbachAlpha();
  
  emit('dragend', props.groupIndex, props.itemIndex, target);
}

async function callCronbachAlpha() {
  try {
    // Generate sample data for demonstration
    // In a real app, you'd get this from your parent component/store
    const sampleData = [
      [5, 4, 3, 5, 4, 3, 2, 4, 5, 3], // Statement 1 responses
      [4, 5, 4, 4, 3, 4, 3, 5, 4, 4], // Statement 2 responses
      [3, 4, 5, 3, 4, 3, 4, 4, 3, 5]  // Statement 3 responses
    ];
    
    const itemDescription = typeof props.item === 'object' 
      ? props.item.displayText 
      : `item ${props.item}`;
    
    console.log(`Calling Cronbach's Alpha for ${itemDescription} in group ${props.groupIndex + 1}`);
    
    // Use the specific cronbach_alpha endpoint (most reliable)
    const result = await apiService.calculateCronbachAlpha(sampleData, props.groupIndex);
    console.log('Cronbach Alpha result:', result);
    
    // Emit the result to parent components
    emit('cronbach-calculated', {
      item: props.item,
      groupIndex: props.groupIndex,
      result: result
    });
    
  } catch (error) {
    console.error('Error calling Cronbach Alpha:', error);
  }
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