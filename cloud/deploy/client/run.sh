#!/usr/bin/env bash
set -eEuo pipefail

cd "$(dirname "$0")"

source ../common/run.sh

common_run "client"
