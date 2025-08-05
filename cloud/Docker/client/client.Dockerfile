FROM node:22.14.0 AS final

WORKDIR /usr/src/app

# Copy static assets (post-build already put HTML into public/)
COPY public ./public

# Copy daemon server code (separate from React's src)
COPY daemon ./daemon

# Copy package.json and package-lock.json to install runtime deps
COPY package*.json ./

RUN npm ci --omit=dev

EXPOSE 8080
CMD ["node", "daemon/daemon.js"]
