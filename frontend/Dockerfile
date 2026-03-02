FROM node:20-alpine AS deps

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules frontend/node_modules
COPY . .

#ARG NEXT_PUBLIC_API_URL=http://localhost:8000
#ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build --prefix frontend

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser  --system --uid 1001 nextjs

#COPY --from=builder /app/public           ./public
COPY --from=builder --chown=nextjs:nodejs /app/frontend/.next/standalone frontend/
COPY --from=builder --chown=nextjs:nodejs /app/frontend/.next/static     frontend/.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "frontend/server.js"]