###################################################
# Stage: base
# 
# This base stage ensures all other stages are using the same base image
# and provides common configuration for all stages, such as the working dir.
###################################################

FROM node:16 as base
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
EXPOSE 8080
CMD [ "node", "src/server.js" ]





###################################################
################  BACKEND STAGES  #################
###################################################

###################################################
# Stage: backend-base
#
# This stage is used as the base for the backend-dev and test stages, since
# there are common steps needed for each.
###################################################
# Google Gemini AI recommened I
# Use a lightweight official Python image as the base
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# in order to have this whole webapp work from one
# instance of google cloud run, need to have the 
# node Express JS serve as a proxy from server to client

# Define the command to run your Flask application
# Using gunicorn for production is recommended, according to Google Cloud
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] 


###################################################
# Sub-Stage: db
#
# This stage is used as the base for the backend-dev and test stages, since
# there are common steps needed for each.
###################################################


###################################################
# Sub-Stage: Seed
#
# This stage is used as the base for the backend-dev and test stages, since
# there are common steps needed for each.
###################################################


###################################################
# Sub-Stage: API
#
# This stage is used as the base for the backend-dev and test stages, since
# there are common steps needed for each.
###################################################



###################################################
# Stage: final
#
# This stage is intended to be the final "production" image. It sets up the
# backend and copies the built client application from the client-build stage.
#
# It pulls the package.json and yarn.lock from the test stage to ensure that
# the tests run (without this, the test stage would simply be skipped).
###################################################
FROM base AS final
ENV NODE_ENV=production
COPY --from=test /usr/local/app/package.json /usr/local/app/yarn.lock ./
RUN --mount=type=cache,id=yarn,target=/usr/local/share/.cache/yarn \
    yarn install --production --frozen-lockfile
COPY backend/src ./src
COPY --from=client-build /usr/local/app/dist ./src/static
EXPOSE 3000
CMD ["node", "src/index.js"]