<template>
  
  <div class="card">
    <div class="card-header text-center">Groep {{ groupIndex + 1 }}</div>
    <div class="card-body">
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
    </div>
    <div class="card-footer text-center">Score: X</div>
  </div>
</template>

<script setup>
import DraggableItem from './DraggableItem.vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  group: Array,
  groupIndex: Number
});

const emit = defineEmits(['dragstart', 'drop']);

function onDragStart(itemIndex) {
  emit('dragstart', props.groupIndex, itemIndex);
}

function onDrop() {
  emit('drop', props.groupIndex);
}
</script>

<style scoped>
.card {
  margin-bottom: 1rem;
}
</style>