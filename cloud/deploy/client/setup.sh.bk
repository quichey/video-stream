#!/usr/bin/env bash

# robust error-handling
set -eEo pipefail

# load utilities and env vars
source util/util.sh
source util/env_vars.sh client

curr_dir=$relative_subdir
location_of_this_script_called='cloud/deploy'
location_of_client_subdir='../../client'

printf "Installing React app dependencies...\n"
cd $location_of_client_subdir
npm install
printf "Completed.\n\n"

# Build frontend HTML (into public/)
printf "Building React frontend and placing into client/public/ ...\n"
npm run build
printf "Completed.\n\n"


printf "Setup completed successfully!\n"

# Back to deploy folder
cd ../${location_of_this_script_called}

case "$DEPLOY_ENV" in
  cloud)
    : "${VERSION:=1}"  # default to 1 if not set

    cp ../Docker/client/client.Dockerfile ../../client/Dockerfile

    gcloud builds submit $location_of_client_subdir \
      --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/client-dev-test:${VERSION}.0.0
    ;;
  local)
    docker build -t client-engine-dev -f ../Docker/client/client.Dockerfile $location_of_client_subdir
    ;;
  *)
    echo "Unknown DEPLOY_ENV: $DEPLOY_ENV"
    exit 1
    ;;
esac
