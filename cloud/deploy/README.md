Collection of Bash scripts for Cloud Deployment

Due to unplanned-go-as-you-code building, and own
conceptual knowledge/programming preferences,
do not have DockerFiles directly in server/ and client/
subdirs. Instead want to "modularize" the different
tools into their own encapsulated folders.

# Just thought of Future Feature (Dev Ops)

Curate (hopefully useful) scripts for quick local developing/debugging


# Enforcing a suitable directory to run the scripts
Hoping to have just one script I can run to setup everything 
for production.

Simplest to me as of now is:
video-stream/cloud/deploy

However, I am building solely the server/setup.sh and 
testing it in isolation to avoid the client-side npm build everytime.
Q: How can I write these scripts to facilitate this?
A?: for development of the server/setup.sh, just run from same subdir