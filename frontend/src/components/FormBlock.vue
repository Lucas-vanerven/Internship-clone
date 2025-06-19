<template>
    //TODO: change 
  <div class="block">
    <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
      <label for="name">Bestand:</label><br>
      <v-file-input label="Selecteer een bestand" variant="outlined" color="primary" class="mb-4" ref="fileInput" @change="handleFileChange" accept=".xlsx"></v-file-input>
      <input 
        type="text" 
        id="name" 
        v-model="formData.name" 
        placeholder="Enter a client"
        required
      >
      <br>
      <input 
        type="file" 
        id="file" 
        ref="fileInput"
        @change="handleFileChange"
        accept=".xlsx" 
        multiple
        style="display:none;"
      >
      <button 
        type="button" 
        id="uploadButton"
        @click="triggerFileSelect"
        class="btn btn-primary"
      >
        <span>{{ selectedFiles.length > 0 ? `${selectedFiles.length} file(s) selected` : 'Select files and combine' }}</span>
      </button>
      <div v-if="selectedFiles.length > 0" class="selected-files">
        <h4>Selected files:</h4>
        <ul>
          <li v-for="file in selectedFiles" :key="file.name">
            {{ file.name }}
          </li>
        </ul>
        <button type="submit" class="btn btn-success">
          Combine Database
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const fileInput = ref(null);
const selectedFiles = ref([]);
const formData = reactive({
  name: ''
});

const triggerFileSelect = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  selectedFiles.value = Array.from(event.target.files);
};

const handleSubmit = async () => {
  if (!formData.name || selectedFiles.value.length === 0) {
    alert('Please enter a name and select at least one file');
    return;
  }

  const formDataToSend = new FormData();
  formDataToSend.append('name', formData.name);
  
  selectedFiles.value.forEach(file => {
    formDataToSend.append('files', file);
  });

  try {
    const response = await fetch('databaseCombiner/api/job/create', {
      method: 'POST',
      body: formDataToSend
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Success:', result);
      // Reset form
      formData.name = '';
      selectedFiles.value = [];
      fileInput.value.value = '';
    } else {
      console.error('Error:', response.statusText);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<style scoped>
.block {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
}

.block label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.block input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 1rem;
  background: var(--color-background);
  color: var(--color-text);
}

.block input[type="text"]:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 0 2px hsla(160, 100%, 37%, 0.2);
}

#uploadButton {
  background: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

#uploadButton:hover {
  background: hsla(160, 100%, 32%, 1);
}

.selected-files {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.selected-files h4 {
  margin-bottom: 0.5rem;
  color: var(--color-heading);
}

.selected-files ul {
  list-style: none;
  padding: 0;
  margin-bottom: 1rem;
}

.selected-files li {
  padding: 0.25rem 0;
  color: var(--color-text-light);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background: hsla(160, 100%, 37%, 1);
  color: white;
}

.btn-primary:hover {
  background: hsla(160, 100%, 32%, 1);
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}
</style>
