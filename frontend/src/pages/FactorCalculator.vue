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
        <GroupsGrid ref="groupsGridRef" />
        
        <div class="footer-section">
          <div class="logo-container">
            <img src="../assets/AR.ico" alt="Company Logo" class="company-logo" />
          </div>
          
          <div class="actions">
            <AnnulerenButton />
            <OpslaanButton @click="handleSaveGroups" />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Page container setup */
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Content area */
.content {
  display: flex;
  flex-direction: column;
  margin: 30px 2% 0 2%;
  flex: 1;
}

main {
  width: 100%;
}

/* Footer section with logo and buttons */
.footer-section {
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 20px;
  padding: 20px 0;
}

/* Logo positioning - centered across full page width */
.logo-container {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 50%;
  transform: translate(-50%, -50%);
}

.company-logo {
  height: 40px;
  width: auto;
}

/* Actions positioned on the right */
.actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 900px) {
  .content {
    margin-right: 10px;
  }
  
  main {
    width: 100%;
  }
  
  .footer-section {
    flex-direction: column;
    gap: 15px;
  }
  
  .actions {
    justify-content: center;
  }
}
</style>
