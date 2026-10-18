export default defineNuxtConfig({
  modules: ['@nuxt/ui'],
  ssr: true,
  runtimeConfig: {
    public: { apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api' }
  }
})
