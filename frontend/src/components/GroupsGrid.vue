<!--
  Groups Grid Component
  
  This component manages the main interface for factor analysis. It provides:
  - Four factor groups where statements can be organized
  - Drag and drop functionality for moving statements between groups
  - Real-time Cronbach's alpha calculation for each group
  - Data persistence to the backend
  
  Key features:
  - Loads statement data from backend based on URL parameters (task_id, client)
  - Calculates reliability scores when groups are modified
  - Provides save functionality for factor groupings
  - Manages drag and drop state across group cards
-->

<template>
  <!-- Grid container for the four factor groups -->
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

// Reactive data for managing four factor groups
const groups = ref([
  [], // Group 1: Statements for first factor
  [], // Group 2: Statements for second factor
  [], // Group 3: Statements for third factor
  []  // Group 4: Statements for fourth factor
]);

// Data loaded from backend for statement management
const displayData = ref([]);
// Cronbach's alpha scores for each group
const groupScores = ref([null, null, null, null]);
// Current item being dragged for drag-and-drop functionality
const draggedItem = ref(null);

// Emit events to parent components for coordination
const emit = defineEmits(['groups-updated', 'scores-calculated', 'save-ready']);

// Expose methods and data to parent components via template refs
defineExpose({
  groups,
  // Extract task ID from URL parameters for backend communication
  getTaskId: () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('task_id') || 'test_task';
  },
  // Extract client identifier from URL parameters
  getClient: () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('client') || 'test_client';
  },
  // Save current factor groups to backend
  saveGroups: async () => {
    const taskId = new URLSearchParams(window.location.search).get('task_id') || 'test_task';
    const client = new URLSearchParams(window.location.search).get('client') || 'test_client';
    
    try {
      const result = await apiService.saveFactorGroups(taskId, client, groups.value);
      console.log('Groups saved successfully:', result);
      return result;
    } catch (error) {
      console.error('Error saving groups:', error);
      throw error;
    }
  }
});

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

// Calculate score for a single group
async function calculateGroupScore(groupIndex) {
  const group = groups.value[groupIndex];
  
  if (group.length < 2) {
    groupScores.value[groupIndex] = null;
    return null;
  }

  try {
    // Get task_id from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('task_id') || 'test_task';
    
    // Extract statement names from the group
    const statementNames = group.map(item => item.original_statement);
    
    // Create groups array - we need to send all groups but we'll only use the result for this group
    const allGroupsStatements = groups.value.map(groupItems => 
      groupItems.map(item => item.original_statement)
    );
    
    const result = await apiService.calculateCronbachAlpha(taskId, allGroupsStatements);
    
    // Extract the score for this specific group - handle null values from backend
    const groupScore = result[groupIndex];
    groupScores.value[groupIndex] = groupScore; // This could be null if group has < 2 statements
    
    console.log(`Group ${groupIndex + 1} Cronbach's Alpha: ${groupScore}`);
    return groupScore !== null ? { cronbach_alpha: groupScore, group_index: groupIndex } : null;
  } catch (error) {
    console.error(`Error calculating score for group ${groupIndex + 1}:`, error);
    groupScores.value[groupIndex] = null;
    return null;
  }
}

// Calculate scores for all groups
async function calculateAllScores() {
  try {
    // Get task_id from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('task_id') || 'test_task';
    
    // Create groups array with statement names
    const allGroupsStatements = groups.value.map(groupItems => 
      groupItems.map(item => item.original_statement)
    );
    
    // Make a single API call for all groups
    const result = await apiService.calculateCronbachAlpha(taskId, allGroupsStatements);
    
    // Update all group scores and collect valid results
    const resultsArray = [];
    for (let groupIndex = 0; groupIndex < groups.value.length; groupIndex++) {
      const groupScore = result[groupIndex];
      groupScores.value[groupIndex] = groupScore; // This could be null for groups with < 2 statements
      
      if (groupScore !== null) {
        resultsArray.push({ cronbach_alpha: groupScore, group_index: groupIndex });
      }
    }
    
    emit('scores-calculated', resultsArray);
    console.log('All group scores calculated:', resultsArray);
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
  grid-gap: 0.5rem;
  gap: 0.5rem;
  margin: 0 auto;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}
</style>