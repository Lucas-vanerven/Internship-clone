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

request = new Request('/api/factorization', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    'id': location.pathname.split('/').pop(),
  })
});

data = fetch(request)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Assuming data is an array of groups
    groups.value = data.groups || [];
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

const groups = ref([
  Array.from({ length: 15 }, (_, i) => i + 1),
  [],
  [],
  []
]);

const draggedItem = ref(null);

function onDragStart(groupIndex, itemIndex) {
  // Set the dragged item to the group and item index
  draggedItem.value = { groupIndex, itemIndex };
}

function onDrop(targetGroupIndex) {
  if (draggedItem.value) {
    const { groupIndex, itemIndex } = draggedItem.value;

    //remove the item from the original group 
    const item = groups.value[groupIndex].splice(itemIndex, 1)[0];
    //add the item to the target group
    groups.value[targetGroupIndex].push(item);

    // Reset the dragged item
    draggedItem.value = null;
    // Log the action
    console.log(`Moved item ${itemIndex} from group ${groupIndex + 1} to group ${targetGroupIndex + 1}`);
  }
}
</script>

<style scoped>


.row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 1rem;
  gap: 1rem;
  margin: 0 auto;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}
</style>