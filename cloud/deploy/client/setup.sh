#!/usr/bin/env bash

# sets bash script environment to be robust w/error-handling
set -eEo pipefail

###########
#
# getting location of where this script is run from
#
###########
source util/util.sh
source util/env_vars.sh client

# location of where this script is run needs to be tracked
curr_dir=$relative_subdir
location_of_this_script_called='cloud/deploy' # adjust if different
location_of_client_subdir='../../client'

########
#
# Automate loading cloud/Docker/...Dockerfiles into 
# correct subdirs such as from cloud/Docker/client/client.Dockerfile into client/Dockerfile
#
########

##
## Hoping I can have just one script to run from here
##


printf "Installing React app dependencies...\n"
cd $location_of_client_subdir
npm install
printf "Completed.\n\n"

printf "Building React app and placing into client/public/. ...\n"
npm run build
printf "Completed.\n\n"

printf "Setup completed successfully!\n"

# back to deploy folder
cd ../${location_of_this_script_called}

case "$DEPLOY_ENV" in
  cloud)
    # set Version
    : "${VERSION:=1}"  # default to 1 if not set

    # Copy Dockerfile from cloud to client folder
    cp ../Docker/client/client.Dockerfile ../../client/Dockerfile

    # Submit cloud build
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

