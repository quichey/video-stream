#!/usr/bin/env bash
set -eEuo pipefail

source ../util/docker_utils.sh

common_run() {
  local target=$1
  echo "[common/run.sh] Running $target..."

  case "$target" in
    client)
      docker run -p 8080:8080 client-engine-dev
      ;;
    server)
      docker run -p 5000:5000 server-engine-dev
      ;;
    *)
      echo "Unknown run target: $target"
      exit 1
      ;;
  esac
}
