FROM node:20 as build
WORKDIR /usr/local/app
RUN ls

# I intend to run this from video-stream/cloud/Docker

# Install the application dependencies
COPY package.json package.json
RUN npm install

#FROM build as install
##RUN npm install
##
##
##
### Copy in the source code
EXPOSE 5000
##
### Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app
##
### TODO: build
CMD ["ls"]


# Dockerfile inheriting from the base image (app.Dockerfile)
#FROM proxy as html