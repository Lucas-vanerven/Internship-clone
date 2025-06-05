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
//defineProps is no longer needed as an import
// import { defineProps, defineEmits } from 'vue';
import DraggableItem from '../DraggableItem.vue';

const props = defineProps({
  group: Array,
  groupIndex: Number
});

const emit = defineEmits(['dragstart', 'drop']);

function onDragStart(groupIndex, itemIndex) {
  emit('dragstart', groupIndex, itemIndex);
}

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