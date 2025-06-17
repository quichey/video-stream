FROM node:20 as build
WORKDIR /usr/local/app
RUN ls

# I intend to run this from video-stream/cloud/Docker

# Install the application dependencies
COPY package.json package.json
RUN npm install

RUN npx create-react-app bullshit
WORKDIR /usr/local/app/bullshit
COPY src src
#RUN npm start || true


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
CMD ["npm", "start"]


# Dockerfile inheriting from the base image (app.Dockerfile)
#FROM proxy as html