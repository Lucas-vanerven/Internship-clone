<template>
  <div class="card">
    <TableHeader :groupIndex="groupIndex" />
    <!-- <v-divider class="border-opacity-100" inset/> --> 
    <div class="card-body">
      <TableBody :group="group" :groupIndex="groupIndex" @dragstart="onDragStart" @drop="onDrop" />
    </div>
    <TableFooter :groupScore="groupScore" />
  </div>
</template>

<script setup>
import TableHeader from './table/TableHeader.vue';
import TableBody from './table/TableBody.vue';
import TableFooter from './table/TableFooter.vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  group: Array,
  groupIndex: Number,
  groupScore: Number
});

const emit = defineEmits(['dragstart', 'drop', 'score-updated']);

function onDragStart(groupIndex, itemIndex) {
  emit('dragstart', groupIndex, itemIndex);
}

function onDrop() {
  emit('drop', props.groupIndex);
}
</script>

<style scoped>
.card {
  margin-bottom: 0.5rem;
  height: 70vh;
}
.card-body {
  padding: 0;
  overflow-y: auto;
  height: 100%;
}
</style>