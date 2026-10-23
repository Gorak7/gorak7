FROM node:20-alpine AS build
WORKDIR /app
ARG VITE_WS_URL=wss://syncboard-api.onrender.com/ws
ENV VITE_WS_URL=$VITE_WS_URL
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1