<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const message = ref("");

    onMounted(async () => {
      const response = await fetch("http://127.0.0.1:8000/");
      const data = await response.json();
      message.value = data.message;
    });

    return { message };
  }
};
</script>
