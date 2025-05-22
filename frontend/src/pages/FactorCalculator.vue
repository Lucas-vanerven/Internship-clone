<script setup>
import GroupsGrid from '../components/GroupsGrid.vue'
import AnnulerenButton from '../components/AnnulerenButton.vue'
import OpslaanButton from '../components/OpslaanButton.vue'
import CreateGroup from '../components/CreateGroup.vue'
import RemoveGroup from '../components/RemoveGroup.vue'
</script>

<template>
  
    <main>
      <GroupsGrid />
    </main>
    

    <div class="management">
      <!-- <CreateGroup />
      <RemoveGroup /> -->
    </div>

    <footer>
      <img alt="Vue logo" class="logo" src="@/assets/AR.ico" width="60" height="60" />
    </footer>

    <div class="actions">
      <AnnulerenButton />
      <OpslaanButton />
    </div>
 
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

main {
  max-height: 100%;
  overflow: auto;
  /* border: 5px solid var(--color-border);
  border-radius: 1rem; */
}

.management, .actions, footer {
  max-height: 10vh;
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
