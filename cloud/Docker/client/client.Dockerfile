FROM node:22.14.0 AS final

WORKDIR /usr/src/app

# Copy static assets (post-build has already placed build output into public/)
COPY public ./public

# Copy runtime server code
COPY src ./src
COPY package*.json ./

EXPOSE 8080
CMD ["node", "daemon/daemon.js"]
