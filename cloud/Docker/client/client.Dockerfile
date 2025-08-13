# Stage 1: Build React app
FROM node:22.14.0 AS builder

WORKDIR /app

# Install all dependencies (dev included)
COPY package*.json ./
RUN npm ci

# Copy everything and build
COPY . .
RUN npm run build

# Stage 2: Runtime image
FROM node:22.14.0 AS final

WORKDIR /usr/src/app

# Install only runtime dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy the built React app from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/build ./public/build

# Copy daemon server code
COPY daemon ./daemon

# Expose the port your server listens on
EXPOSE 8080

# Start the daemon
CMD ["node", "daemon/daemon.js"]