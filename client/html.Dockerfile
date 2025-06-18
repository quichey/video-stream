## STAGE use node/linux thing

FROM node:20 as build
WORKDIR /usr/local/app
RUN ls

# I intend to run this from video-stream/cloud/Docker

## STAGE set-up react app
# Install the application dependencies
FROM build as react-install
COPY package.json package.json
RUN npm install

RUN npx create-react-app bullshit
WORKDIR /usr/local/app/bullshit
COPY src src
#RUN npm start || true


# Dockerfile inheriting from the base image (app.Dockerfile)
#FROM proxy as html

## STAGE build production
FROM react-install as prod-build
RUN npm run build
#RUN npm install -g server
RUN npm install server
RUN serve -s build

## STAGE install snapd for server?
#FROM prod-build as snap-install
#RUN apt update
#RUN apt install -y snapd squashfuse fuse
#RUN systemctl enable snapd
#RUN systemctl start snapd.service
#CMD ["ls"]

## STAGE start up server
#FROM snap-install as server-start
#RUN snap install server
#RUN serve -s build

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

