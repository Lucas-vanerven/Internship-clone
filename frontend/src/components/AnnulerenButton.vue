<!--
  Annuleren (Cancel) Button Component
  
  A simple cancel button component used in the factor analysis interface.
  Displays "Annuleren" (Dutch for "Cancel") and provides a secondary 
  styling to indicate it's not the primary action.
  
  Currently displays as a static button without click handlers.
  Future enhancement could add functionality to reset or cancel operations.
-->

<template>
  <button class="btn btn-secondary me-2">Annuleren</button>
</template>

<script>
export default {
  name: 'AnnulerenButton'
};
</script>

<style scoped>
/* Add any specific styles for the Annuleren button here */

</style>