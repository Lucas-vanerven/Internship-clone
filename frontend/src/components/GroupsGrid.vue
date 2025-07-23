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
import { ref, watch, defineEmits, onMounted } from 'vue';
import GroupCard from './GroupCard.vue';
import apiService from '../services/apiService.js';

const groups = ref([
  [],
  [],
  [],
  []
]);

const displayData = ref([]);
const groupScores = ref([null, null, null, null]);
const draggedItem = ref(null);

// Emit events to parent components
const emit = defineEmits(['groups-updated', 'scores-calculated']);

// Fetch display data from the backend
async function fetchDisplayData() {
  try {
    // Get task_id and client from URL query parameters or use defaults for testing
    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('task_id') || 'test_task';
    const client = urlParams.get('client') || 'test_client';
    
    console.log(`Fetching display data for task_id: ${taskId}, client: ${client}`);
    
    const data = await apiService.getDisplayData(taskId, client);
    displayData.value = data;
    
    // Organize statements into groups based on factor_groups
    organizeStatementsIntoGroups(data);
    
    console.log('Display data fetched:', data);
  } catch (error) {
    console.error('Error fetching display data:', error);
    // Fallback to test data if API fails
    displayData.value = [
      { original_statement: "Test statement 1", aliasses: "Test alias 1", factor_groups: 1 },
      { original_statement: "Test statement 2", aliasses: "Test alias 2", factor_groups: 2 }
    ];
    organizeStatementsIntoGroups(displayData.value);
  }
}

// Organize statements into groups based on factor_groups
function organizeStatementsIntoGroups(data) {
  // Reset all groups
  groups.value = [[], [], [], []];
  
  data.forEach((statement, index) => {
    const groupIndex = statement.factor_groups - 1; // Convert to 0-based index
    
    // Ensure we have a valid group index (0-3)
    if (groupIndex >= 0 && groupIndex < 4) {
      groups.value[groupIndex].push({
        id: index,
        original_statement: statement.original_statement,
        aliasses: statement.aliasses,
        factor_groups: statement.factor_groups,
        displayText: statement.aliasses || statement.original_statement
      });
    } else {
      // If factor_groups is out of range, put it in the first group
      groups.value[0].push({
        id: index,
        original_statement: statement.original_statement,
        aliasses: statement.aliasses,
        factor_groups: statement.factor_groups,
        displayText: statement.aliasses || statement.original_statement
      });
      console.warn(`Statement with factor_groups ${statement.factor_groups} placed in group 1`);
    }
  });
  
  console.log('Organized groups:', groups.value);
}

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

// Initialize component
onMounted(async () => {
  await fetchDisplayData();
  // Calculate initial scores after data is loaded
  calculateAllScores();
});
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