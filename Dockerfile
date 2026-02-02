# Multi-stage build for backend
FROM node:18-alpine AS backend
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm install --production
COPY backend/ ./
EXPOSE 4000
CMD ["npm", "start"]
