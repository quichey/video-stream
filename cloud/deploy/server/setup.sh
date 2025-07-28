#!/usr/bin/env bash

# WHERE SHOULD I RUN THIS COMMAND FROM?
# video-stream/cloud ?

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# sets bash script environment to be robust w/error-handling
set -eEo pipefail



###########
#
# getting location of where this script is run from
#
###########
source util/util.sh

# location of where this script is run needs to be tracked
curr_dir=$relative_subdir
location_of_this_script_called='video-stream/cloud/deploy' #w/in deploy/setup.sh
location_of_server_subdir='../../server'


########
#
# want to automate loading cloud/Docker/...Dockerfiles into 
# correct subdirs such as from cloud/Docker/server/server.Dockerfile into server/Dockerfile
#
########
#cd ../server
#cp ../cloud/Docker/server/server.Dockerfile ./Dockerfile # run Docker from here instead?

# run this from video-stream/server folder
case "$DEPLOY_ENV" in
  cloud)
    gcloud builds submit $location_of_server_subdir \
      --config ../Docker/server/cloudbuild.yaml
    ;;
  local)
    docker build -t server-engine-dev -f ../Docker/server/server.Dockerfile $location_of_server_subdir
    ;;
  *)
    echo "Unknown DEPLOY_ENV: $DEPLOY_ENV"
    exit 1
    ;;
esac

#
# FORGOT: google cloud uses different command to build docker
#