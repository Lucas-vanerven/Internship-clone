<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { ref } from 'vue'
import GroupsGrid from './components/GroupsGrid.vue'
import AnnulerenButton from './components/AnnulerenButton.vue'
import OpslaanButton from './components/OpslaanButton.vue'
import CreateGroup from './components/CreateGroup.vue'
import RemoveGroup from './components/RemoveGroup.vue'
</script>

<template>
  <!-- <div class="container mt-5"> -->
    <!-- <header class="text-center mb-4">
      <img alt="Vue logo" class="logo" src="@/assets/AR.ico" width="125" height="125" />
    </header> -->
    <main>
      <GroupsGrid />
    </main>
    

    <!-- TODO: Center the elements with css somehow ;) in main.css -->
    <div class="management">
      <CreateGroup />
      <RemoveGroup />
    </div>

    <footer>
      <img alt="Vue logo" class="logo" src="@/assets/AR.ico" width="125" height="125" />
    </footer>

    <div class="actions">
      <!-- TODO: Replace these buttons with the correct ones -->
      <AnnulerenButton />
      <OpslaanButton />
    </div>
  <!-- </div> -->
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.sidewrapper {
  grid-template-rows: 300px 600px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
