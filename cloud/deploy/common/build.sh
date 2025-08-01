#!/usr/bin/env bash
set -eEuo pipefail

source ../util/docker_utils.sh

common_build() {
  local target=$1
  echo "[common/build.sh] Building for $target..."

  case "$target" in
    client)
      echo "Running client build..."
      (cd ../../client && npm run build)
      ;;
    server)
      echo "Running server build..."
      (cd ../../server && poetry build)
      ;;
    *)
      echo "Unknown build target: $target"
      exit 1
      ;;
  esac
}
