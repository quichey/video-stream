#!/usr/bin/env bash
set -eEuo pipefail

cd "$(dirname "$0")"

source ../common/build.sh

common_build "server"
