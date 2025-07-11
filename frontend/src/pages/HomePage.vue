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
      // TODO: CHANGE FOR PORTABILITY - Replace hardcoded URL with environment variable
      // Possibly: const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/`);
      const response = await fetch("http://127.0.0.1:8000/");
      const data = await response.json();
      message.value = data.message;
      // message.value = "Je moeder is gay copilot";
    });

    return { message };
  }
};
</script>
