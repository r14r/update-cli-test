export default defineEventHandler(async (event) => {
  const path = getRouterParam(event, 'path') || ''
  const base = process.env.BACKEND_URL || 'http://backend:8000'
  return proxyRequest(event, `${base}/api/${path}`)
})
