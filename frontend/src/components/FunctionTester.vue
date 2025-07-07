<template>
  <div class="function-tester">
    <h3>Backend Function Tester</h3>
    
    <div class="controls">
      <button @click="listFunctions" class="btn btn-info">List Available Functions</button>
      <button @click="testCronbachAlpha" class="btn btn-primary">Test Cronbach's Alpha</button>
      <button @click="testDescriptiveStats" class="btn btn-secondary">Test Descriptive Statistics</button>
      <button @click="testCorrelationMatrix" class="btn btn-success">Test Correlation Matrix</button>
      <button @click="testItemAnalysis" class="btn btn-warning">Test Item Analysis</button>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Loading...</p>
    </div>
    
    <div v-if="result" class="result">
      <h4>Result:</h4>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
    
    <div v-if="error" class="error">
      <h4>Error:</h4>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import apiService from '../services/apiService.js';

const loading = ref(false);
const result = ref(null);
const error = ref(null);

// Sample data for testing
const sampleData = [
  [5, 4, 3, 5, 4, 3, 2, 4, 5, 3], // Statement 1 responses
  [4, 5, 4, 4, 3, 4, 3, 5, 4, 4], // Statement 2 responses
  [3, 4, 5, 3, 4, 3, 4, 4, 3, 5], // Statement 3 responses
  [5, 3, 4, 5, 5, 2, 3, 4, 5, 4]  // Statement 4 responses
];

async function callFunction(functionName, description) {
  loading.value = true;
  error.value = null;
  result.value = null;
  
  try {
    console.log(`Testing ${functionName}: ${description}`);
    const response = await apiService.callFunction(functionName, {
      group_data: sampleData
    });
    result.value = response;
    console.log(`${functionName} result:`, response);
  } catch (err) {
    error.value = err.message;
    console.error(`Error calling ${functionName}:`, err);
  } finally {
    loading.value = false;
  }
}

async function listFunctions() {
  loading.value = true;
  error.value = null;
  result.value = null;
  
  try {
    const functions = await apiService.listAvailableFunctions();
    result.value = { available_functions: functions };
    console.log('Available functions:', functions);
  } catch (err) {
    error.value = err.message;
    console.error('Error listing functions:', err);
  } finally {
    loading.value = false;
  }
}

async function testCronbachAlpha() {
  await callFunction('cronbach_alpha', 'Calculate Cronbach\'s alpha for reliability analysis');
}

async function testDescriptiveStats() {
  await callFunction('descriptive_statistics', 'Calculate descriptive statistics');
}

async function testCorrelationMatrix() {
  await callFunction('correlation_matrix', 'Calculate correlation matrix');
}

async function testItemAnalysis() {
  await callFunction('item_analysis', 'Perform item analysis');
}
</script>

<style scoped>
.function-tester {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin: 1rem 0;
}

.controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.controls button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: white;
}

.btn-info { background-color: #17a2b8; }
.btn-primary { background-color: #007bff; }
.btn-secondary { background-color: #6c757d; }
.btn-success { background-color: #28a745; }
.btn-warning { background-color: #ffc107; color: #212529; }

.loading {
  color: #007bff;
  font-style: italic;
}

.result {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
  color: #000000;
}

.result pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
}

.error {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
}
</style>
