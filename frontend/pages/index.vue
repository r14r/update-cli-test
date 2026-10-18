<script setup lang="ts">
const { data: message, error } = await useFetch<{ message: string }>('/api/message')
</script>
<template>
  <main class="max-w-3xl mx-auto p-10 space-y-5">
    <UCard>
      <template #header><h1 class="text-2xl font-bold">Update CLI Test</h1></template>
      <p>FastAPI + Vue/Nuxt UI integration fixture</p>
      <p data-testid="message">{{ message?.message ?? (error ? 'Backend unavailable' : 'Loading...') }}</p>
      <UButton to="/api/health" target="_blank">API health</UButton>
    </UCard>
  </main>
</template>
