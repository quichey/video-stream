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


#printf "Installing monolith dependencies...\n"
#cd ./monolith
#npm install
#printf "Completed.\n\n"

#printf "Installing microservices dependencies...\n"
#cd ../microservices
#npm install
#printf "Completed.\n\n"


##
## Hoping I can have just one script to run from here
##


printf "Installing React app dependencies...\n"
cd ../client
npm install
printf "Completed.\n\n"

printf "Building React app and placing into client/public/. ...\n"
npm run build
printf "Completed.\n\n"

printf "Setup completed successfully!\n"

########
#
# want to automate loading cloud/Docker/...Dockerfiles into 
# correct subdirs such as from cloud/Docker/client/HTML/tutorial.Dockerfile into client/Dockerfile
#
########
cp ../cloud/Docker/client/HTML/tutorial.Dockerfile ./Dockerfile


docker build -t client-engine-dev -f ./mysql/mysql-v2.Dockerfile .
