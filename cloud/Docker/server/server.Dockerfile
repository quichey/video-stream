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
COPY env ./

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
# TODO: I think update this line to not include the local machine's poetry installation or something
COPY . .
#COPY api/poetry.lock ./ # somehow no poetry.lock in here
# Q: Which of the above 2 do i need?

#RUN pip install poetry
#RUN pip install --upgrade pip && pip install --upgrade poetry
RUN pip install poetry==2.1.1

#RUN poetry install --no-root
RUN poetry install --no-root --no-interaction --no-ansi
#RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN python -m poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN pip install -r requirements.txt


# Copy in the source code
#TODO: do copy of source code -- ran local test of this file
#EXPOSE 5000
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd -m app
USER app

# Make sure pip-installed executables are on PATH
ENV PATH="/usr/local/bin:${PATH}"

###
#
# STAGE: start up flask server
#
##

#CMD ["flask", "--app", "api", "run"]
#CMD ["flask", "--app", "api", "run", "--host=0.0.0.0"]

# this one worked before
#CMD ["poetry", "run", "flask", "--app", "api", "run", "--host=0.0.0.0", "--port=8080"]

# trying out this one from CHATGPT suggestion
CMD ["python", "main.py"]



