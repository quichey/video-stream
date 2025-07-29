#!/usr/bin/env bash
set -eEuo pipefail

BASE_DOCKERFILE="../Docker/server/server.Dockerfile"

# set Version
: "${VERSION:=1}"  # default to 1 if not set
# Make a copy of the base Dockerfile
TEMP_DOCKERFILE="../Docker/server/server.cloud.Dockerfile"

# Insert proxy install lines before CMD
awk '
/^CMD/ {
    print "RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /usr/local/bin/cloud_sql_proxy && chmod +x /usr/local/bin/cloud_sql_proxy"
}
{ print }
' "$BASE_DOCKERFILE" > "$TEMP_DOCKERFILE"

gcloud builds submit ../../server \
--tag gcr.io/${GOOGLE_CLOUD_PROJECT}/server-dev-test:${VERSION}.0.0