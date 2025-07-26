#!/usr/bin/env bash

set -e

###########
#
# getting location of where this script is run from
#
###########

get_curr_subdir() {
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    relative_subdir="${script_dir/#$PWD\//}"
    echo "relative_subdir: ${relative_subdir}"
}

get_curr_subdir


###########
#
# DETECT MACHINE
#
###########
: "${DEPLOY_ENV:=local}"  # default to local if not set

case "$DEPLOY_ENV" in
  cloud)
    echo "Cloud setup"
    SERVER_HOST="cloud-db.example.com"
    ;;
  local)
    echo "Local setup"
    SERVER_HOST="localhost"
    ;;
  *)
    echo "Unknown DEPLOY_ENV: $DEPLOY_ENV"
    exit 1
    ;;
esac
