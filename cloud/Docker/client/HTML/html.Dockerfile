FROM node:20 as build
WORKDIR /usr/local/app

# I intend to run this from video-stream/cloud/Docker

# Install the application dependencies
COPY ~/repos/video-stream/client ./client
RUN npm install



# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# TODO: build
CMD ["npm", "build"]


# Dockerfile inheriting from the base image (app.Dockerfile)
FROM proxy:latest as html