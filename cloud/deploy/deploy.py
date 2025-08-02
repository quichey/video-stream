#!/usr/bin/env bash
set -eEo pipefail

ENVIRONMENT=${1:-local}  # default to local if not specified
SYSTEM_PACKAGE="package-name"

CLIENT_DIR="./client"
SERVER_DIR="./server"

install_system_packages() {
  echo "Installing system packages (only for cloud)..."
  export DEBIAN_FRONTEND=noninteractive
  sudo apt-get update -q
  sudo apt-get install -y -q "$SYSTEM_PACKAGE"
  unset DEBIAN_FRONTEND
  echo "System packages installed."
}

install_client_dependencies() {
  echo "Installing npm dependencies for client..."
  cd "$CLIENT_DIR"
  npm install --yes --quiet
  cd - > /dev/null
}

install_server_dependencies() {
  echo "Installing Python dependencies for server..."
  cd "$SERVER_DIR"
  poetry install --no-interaction --no-ansi --quiet
  cd - > /dev/null
}

deploy_client() {
  echo "Running client setup..."
  "$CLIENT_DIR/setup.sh"
  echo "Running client build..."
  "$CLIENT_DIR/build.sh"
  echo "Running client run..."
  "$CLIENT_DIR/run.sh"
  echo "Client deployed and running."
}

deploy_server() {
  echo "Running server setup..."
  "$SERVER_DIR/setup.sh"
  echo "Running server build..."
  "$SERVER_DIR/build.sh"
  echo "Running server run..."
  "$SERVER_DIR/run.sh"
  echo "Server deployed and running."
}

main() {
  if [ "$ENVIRONMENT" = "cloud" ]; then
    install_system_packages
  else
    echo "Skipping system package installation (local mode)."
  fi

  install_client_dependencies
  install_server_dependencies
  deploy_client
  deploy_server

  echo "Deployment completed successfully in $ENVIRONMENT mode."
}

main
