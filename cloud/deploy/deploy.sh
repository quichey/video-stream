#!/usr/bin/env bash
set -eEuo pipefail

cd "$(dirname "$0")"

deploy_component() {
  local component=$1
  echo ">>> Setting up $component..."
  bash "$component/setup.sh"

  echo ">>> Building $component..."
  bash "$component/build.sh"

  echo ">>> Running $component..."
  bash "$component/run.sh"

  echo ">>> $component deployed successfully."
}

echo "=== Starting full deploy sequence ==="

deploy_component client
deploy_component server

echo "=== Deploy sequence complete ==="
