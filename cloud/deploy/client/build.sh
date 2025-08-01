#!/usr/bin/env bash
set -eEuo pipefail

# Navigate to this script's directory
cd "$(dirname "$0")"

# Source the shared build logic
source ../common/build.sh

# Run the common build for client
common_build "client"
