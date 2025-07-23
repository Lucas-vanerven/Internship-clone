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
  
  emit('dragstart', props.groupIndex, props.itemIndex);
}

async function onDragEnd(event) {
  console.log("Drag ended");
  const target = event.relatedTarget?.closest('ul'); // Use relatedTarget to get the drop target
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