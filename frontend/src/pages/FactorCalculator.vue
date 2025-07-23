<script setup>
import { ref } from 'vue';
import GroupsGrid from '../components/GroupsGrid.vue'
import AnnulerenButton from '../components/AnnulerenButton.vue'
import OpslaanButton from '../components/OpslaanButton.vue'
import CreateGroup from '../components/CreateGroup.vue'
import RemoveGroup from '../components/RemoveGroup.vue'

// Create a reference to the GroupsGrid component
const groupsGridRef = ref(null);

// Function to handle saving factor groups
async function handleSaveGroups() {
  if (groupsGridRef.value) {
    try {
      const result = await groupsGridRef.value.saveGroups();
      console.log('Factor groups saved successfully!', result);
      alert('Factor groups saved successfully!');
      return result;
    } catch (error) {
      console.error('Error saving factor groups:', error);
      alert('Error saving factor groups: ' + error.message);
      throw error;
    }
  } else {
    console.error('GroupsGrid reference not available');
    alert('Error: Cannot access groups data');
  }
}
</script>

<template>
  <div class="page-container">
    <div class="content">
      <main class="block">
        <h2>Factor Group Calculator</h2>
        <GroupsGrid ref="groupsGridRef" />
      </main>
    </div>
    
    <div class="actions">
      <AnnulerenButton />
      <OpslaanButton @click="handleSaveGroups" />
    </div>
  </div>
</template>

<style scoped>
/* Page container setup */
.page-container {
  min-height: 100vh;
  display: flex;
  position: relative;
}

/* Content area */
.content {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  margin: 30px 2% 0 2%;
  flex: 1;
}

main {
  flex-grow: 2;
  width: 100%;
  max-width: 70%;
}

/* Actions positioned on the right */
.actions {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
  z-index: 10;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column;
    margin-right: 10px;
  }
  
  main {
    width: 100%;
    max-width: 98%;
  }
  
  .actions {
    position: relative;
    bottom: auto;
    right: auto;
    justify-content: center;
    margin-top: 20px;
  }
}
</style>
