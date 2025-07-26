###############################################################
#
# TRY TO MAKE SAME AS LOCAL SETUP FOR RUNNING API
#
# STAGES:
# 1) prepare environment for connecting to g-cloud-sql instance
# 2) Run Seed program -- NOT NEEDED (OPTIONAL)
# 3) start up API
#
#
#
#
###############################################################

FROM python:3.10.12
WORKDIR /usr/local/app
ARG APP_DIR=../../server
# I intend to run this from video-stream/cloud/Docker

########
#
# Stage
# prep environment for connecting to g-cloud-sql instance
#
# copy over .env file?
# 
########

########
#
# Stage
# Run Seed program -- NOT NEEDED (OPTIONAL)
#
########


########
#
# Stage
# start up API
#
# do python/poetry packaging things
# do flask things
#
########

# Install the application dependencies
COPY pyproject.toml ./
COPY poetry.lock ./
COPY README.md ./

# attempt fix 'cannot import api module' error
COPY . .
#COPY api/poetry.lock ./ # somehow no poetry.lock in here
# Q: Which of the above 2 do i need?

#RUN pip install poetry
#RUN pip install --upgrade pip && pip install --upgrade poetry
RUN pip install poetry==1.8.3

#RUN poetry install --no-root
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN pip install -r requirements.txt


# Copy in the source code
#TODO: do copy of source code -- ran local test of this file
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# start up flask server
#CMD ["flask", "--app", "api", "run"]
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]



