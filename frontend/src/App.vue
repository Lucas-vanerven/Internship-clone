<!--
  Root Vue Component (App.vue)
  
  This is the main application component that serves as the entry point
  for the entire Vue.js application. Currently, it directly renders
  the FactorCalculator component as the main interface.
  
  Note: This bypasses the router system and directly displays the
  factor calculation interface.
-->

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FactorCalculator from './pages/FactorCalculator.vue';
</script>

<template>
  <!-- Main application content - currently showing FactorCalculator directly -->
  <FactorCalculator /> 
</template>