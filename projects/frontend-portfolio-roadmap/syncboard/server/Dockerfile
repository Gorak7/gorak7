FROM node:20-bookworm-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

FROM node:20-bookworm-slim
ENV NODE_ENV=production
WORKDIR /app
RUN mkdir -p /var/data && chown -R node:node /var/data /app
COPY --from=build --chown=node:node /app/package*.json ./
RUN npm install --omit=dev
COPY --from=build --chown=node:node /app/dist ./dist
USER node
ENV PORT=3001
ENV SQLITE_PATH=/var/data/syncboard.sqlite
EXPOSE 3001
CMD ["node","dist/index.js"]