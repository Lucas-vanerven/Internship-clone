<template>
  
    <div class="row">
      <GroupCard
        v-for="(group, index) in groups"
        :key="index"
        :group="group"
        :groupIndex="index"
        :groupScore="groupScores[index]"
        @dragstart="onDragStart"
        @drop="onDrop"
        @score-updated="handleScoreUpdate"
      />   
  </div>
  
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';
import GroupCard from './GroupCard.vue';
import apiService from '../services/apiService.js';

// request = new Request('/api/factorization', {
//   method: 'GET',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify({
//     'id': location.pathname.split('/').pop(),
//   })
// });

// data = fetch(request)
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return response.json();
//   })
//   .then(data => {
//     // Assuming data is an array of groups
//     groups.value = data.groups || [];
//   })
//   .catch(error => {
//     console.error('There was a problem with the fetch operation:', error);
//   });

const groups = ref([
  Array.from({ length: 15 }, (_, i) => i + 1),
  [],
  [],
  []
]);

const groupScores = ref([null, null, null, null]);
const draggedItem = ref(null);

// Emit events to parent components
const emit = defineEmits(['groups-updated', 'scores-calculated']);

// Generate mock data for statements (this would come from your actual data)
const generateMockData = (statements) => {
  // Generate random scores for each statement (1-5 scale, simulating Likert responses)
  return statements.map(() => 
    Array.from({ length: 10 }, () => Math.floor(Math.random() * 5) + 1) // 10 responses per statement
  );
};

// Calculate score for a single group
async function calculateGroupScore(groupIndex) {
  const group = groups.value[groupIndex];
  
  if (group.length < 2) {
    groupScores.value[groupIndex] = null;
    return null;
  }

  try {
    // Generate mock data for the statements in this group
    const mockData = generateMockData(group);
    
    const result = await apiService.calculateCronbachAlpha(mockData, groupIndex);
    groupScores.value[groupIndex] = result.cronbach_alpha;
    
    console.log(`Group ${groupIndex + 1} Cronbach's Alpha: ${result.cronbach_alpha}`);
    return result;
  } catch (error) {
    console.error(`Error calculating score for group ${groupIndex + 1}:`, error);
    groupScores.value[groupIndex] = null;
    return null;
  }
}

// Calculate scores for all groups
async function calculateAllScores() {
  try {
    const allGroupsData = groups.value.map(group => {
      if (group.length >= 2) {
        return generateMockData(group);
      }
      return [];
    });

    const result = await apiService.calculateAllGroupsScores(allGroupsData);
    
    // Update group scores
    result.results.forEach((groupResult) => {
      groupScores.value[groupResult.group_index] = groupResult.cronbach_alpha;
    });
    
    emit('scores-calculated', result.results);
    console.log('All group scores calculated:', result.results);
  } catch (error) {
    console.error('Error calculating all group scores:', error);
  }
}

function onDragStart(groupIndex, itemIndex) {
  // Set the dragged item to the group and item index
  draggedItem.value = { groupIndex, itemIndex };
}

async function onDrop(targetGroupIndex) {
  if (draggedItem.value) {
    const { groupIndex, itemIndex } = draggedItem.value;

    //remove the item from the original group 
    const item = groups.value[groupIndex].splice(itemIndex, 1)[0];
    //add the item to the target group
    groups.value[targetGroupIndex].push(item);

    // Reset the dragged item
    draggedItem.value = null;
    
    // Calculate new scores for affected groups
    await calculateGroupScore(groupIndex); // Original group
    await calculateGroupScore(targetGroupIndex); // Target group
    
    // Emit update event
    emit('groups-updated', groups.value);
    
    // Log the action
    console.log(`Moved item ${itemIndex} from group ${groupIndex + 1} to group ${targetGroupIndex + 1}`);
  }
}

function handleScoreUpdate(groupIndex) {
  calculateGroupScore(groupIndex);
}

// Watch for changes in groups and recalculate scores
watch(groups, () => {
  emit('groups-updated', groups.value);
}, { deep: true });

// Calculate initial scores
calculateAllScores();
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