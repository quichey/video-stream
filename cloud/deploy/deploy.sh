#!/usr/bin/env bash
set -eEuo pipefail

# Navigate to the directory of this script
cd "$(dirname "$0")"

usage() {
  echo "Usage: $0 {setup|build|run} [client|server|all]"
  echo "  setup|build|run : command to run"
  echo "  client|server|all : target (default: all)"
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi

COMMAND=$1
TARGET=${2:-all}

run_script() {
  local component=$1
  local command=$2
  echo "=== Running $command for $component ==="
  bash "$component/$command.sh"
  echo "=== Completed $command for $component ==="
  echo
}

case "$COMMAND" in
  setup|build|run)
    case "$TARGET" in
      client)
        run_script client $COMMAND
        ;;
      server)
        run_script server $COMMAND
        ;;
      all)
        run_script client $COMMAND
        run_script server $COMMAND
        ;;
      *)
        echo "Invalid target: $TARGET"
        usage
        ;;
    esac
    ;;
  *)
    echo "Invalid command: $COMMAND"
    usage
    ;;
esac
