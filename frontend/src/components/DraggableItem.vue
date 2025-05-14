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


function onDragEnd(event) {
  console.log("Drag ended");
  const target = event.relatedTarget?.closest('ul'); // Use relatedTarget to get the drop target
  console.log("Dropped on target:", target);
  emit('dragend', props.groupIndex, props.itemIndex, target);
}

</script>

<style scoped>
.list-group-item {
  cursor: grab;
}
</style>