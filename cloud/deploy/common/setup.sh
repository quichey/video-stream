#!/usr/bin/env bash
set -eEuo pipefail

# Import shared utility functions
source ../util/docker_utils.sh
source ../util/git_utils.sh

# Function to handle common setup tasks
common_setup() {
  local target=$1
  echo "[common/setup.sh] Setting up for $target..."

  ensure_clean_working_tree

  # Target-specific logic
  case "$target" in
    client)
      echo "Installing dependencies for client..."
      (cd ../../client && npm install)
      ;;
    server)
      echo "Installing dependencies for server..."
      (cd ../../server && poetry install)
      ;;
    *)
      echo "Unknown setup target: $target"
      exit 1
      ;;
  esac
}
