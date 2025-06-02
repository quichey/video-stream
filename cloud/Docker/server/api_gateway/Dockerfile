FROM python:3.10.12
WORKDIR /usr/local/app

# I intend to run this from video-stream/cloud/Docker

# Install the application dependencies
COPY ~/repos/video-stream/server ./server
RUN pip install poetry
RUN poetry install

 
# ---- figure out how to do it w/out python interpreter

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# start up flask server
CMD ["flask", "--app", "api", "run"]