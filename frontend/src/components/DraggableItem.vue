<template>
  <li
    class="list-group-item"
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
  >
    Stelling {{ item }}
  </li>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  item: Number,
  groupIndex: Number,
  itemIndex: Number
});

const emit = defineEmits(['dragstart', 'dragend']);

function onDragStart() {
  console.log("Drag started - asdfafß")
  emit('dragstart', props.groupIndex, props.itemIndex);
}


function onDragEnd() {
  console.log("Drag ended");	
  emit('dragend', props.groupIndex, props.itemIndex);
}

</script>

<style scoped>
.list-group-item {
  cursor: grab;
}
</style>