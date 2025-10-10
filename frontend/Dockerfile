# Multi-stage build for React/Vite frontend
FROM node:21-alpine as build

# Set working directory
WORKDIR /app

# Update npm to compatible version for Node 18
RUN npm install -g npm@10 --unsafe-perm=true --allow-root

# Copy package files
COPY package*.json ./

# Clean npm cache and install all dependencies (including dev dependencies for build)
RUN npm cache clean --force
RUN rm -rf node_modules package-lock.json
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
