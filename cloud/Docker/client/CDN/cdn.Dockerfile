FROM python:3.10.12 as build
#Assuming proxy was built from util.daemon.Dockerfile
WORKDIR /usr/local/app
RUN ls

# I intend to run this from video-stream/cloud/Docker

# Install the application dependencies


# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# TODO: build
CMD ["npm", "build"]


# Dockerfile inheriting from the base image (app.Dockerfile)
FROM proxy:latest as cdn