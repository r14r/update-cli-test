FROM node:22-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install --no-audit --no-fund --loglevel=error
COPY frontend/ ./
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/.output ./.output
ENV HOST=0.0.0.0 PORT=3000 BACKEND_URL=http://backend:8000
EXPOSE 3000
HEALTHCHECK --interval=10s --timeout=3s --retries=8 CMD node -e 'fetch("http://127.0.0.1:3000").then(r=>{if(!r.ok)process.exit(1)}).catch(()=>process.exit(1))'
CMD ["node", ".output/server/index.mjs"]
