<!--
  Upload Page Component
  
  This page provides the initial data upload interface for the Cronbach's alpha
  web application. Users can upload their datasets here to begin factor analysis.
  
  The page serves as a container for the NewJobForm component which handles
  the actual file upload functionality and job creation.
  
  Note: Currently references a NewJobForm component that may not exist in the
  current codebase structure.
-->

<script setup lang="ts">
// TypeScript setup - no additional imports currently needed
</script>

<template>
    <!-- Main upload form component -->
    <NewJobForm />
</template>

<style>
@media (min-width: 1024px) {
  .UploadPage {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
