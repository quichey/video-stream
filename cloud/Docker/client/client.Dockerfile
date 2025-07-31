###################################################
# Stage: base
# 
# This base stage ensures all other stages are using the same base image
# and provides common configuration for all stages, such as the working dir.
###################################################

FROM node:22.14.0 as base
WORKDIR /usr/src/app

################## CLIENT STAGES ##################

###################################################
# Stage: client-base
#
# This stage is used as the base for the client-dev and client-build stages,
# since there are common steps needed for each.
###################################################
FROM base AS client-base

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

###################################################
# Stage: client-build
#
# This stage builds the client application, producing static HTML, CSS, and
# JS files that can be served by the backend.
###################################################
FROM client-base AS client-build

# Build React app
RUN npm run build

# Expose port if needed (not usually required in build stage)
EXPOSE 8080

# No CMD here because this stage is only for building

###################################################
# Stage: final
#
# This stage is intended to be the final "production" image.
###################################################
FROM base AS final

ENV NODE_ENV=production

# Copy package files for production dependencies
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Copy all source files, including the public folder which post-build.js
# ensures contains the built React app
COPY . .

EXPOSE 8080

# Run your server (renamed daemon.js as you mentioned)
CMD ["node", "src/daemon.js"]
