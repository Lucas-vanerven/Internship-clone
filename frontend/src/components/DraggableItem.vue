<template>
  <li
    class="list-group-item"
    draggable="true"
    @dragstart="onDragStart"
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

const emit = defineEmits(['dragstart']);

function onDragStart() {
  emit('dragstart', groupIndex, itemIndex);
}
</script>

<style scoped>
.list-group-item {
  cursor: grab;
}
</style>