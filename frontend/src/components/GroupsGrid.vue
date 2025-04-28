<template>
  <div class="row">
    <GroupCard
      v-for="(group, index) in groups"
      :key="index"
      :group="group"
      :groupIndex="index"
      @dragstart="onDragStart"
      @drop="onDrop"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import GroupCard from './GroupCard.vue';

const groups = ref([
  Array.from({ length: 15 }, (_, i) => i + 1),
  [],
  [],
  []
]);

const draggedItem = ref(null);

function onDragStart(groupIndex, itemIndex) {
  draggedItem.value = { groupIndex, itemIndex };
}

function onDrop(targetGroupIndex) {
  if (draggedItem.value) {
    const { groupIndex, itemIndex } = draggedItem.value;
    const item = groups.value[groupIndex].splice(itemIndex, 1)[0];
    groups.value[targetGroupIndex].push(item);
    draggedItem.value = null;
  }
}
</script>

<style scoped>
.row {
  display: flex;
  flex-wrap: wrap;
}
</style>