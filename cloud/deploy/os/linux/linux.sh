#!/usr/bin/env bash

# Detect whether we are in a cloud environment or local
detect_env_type() {
  # Option 1: Use GOOGLE_CLOUD_PROJECT as indicator (Cloud Build / Cloud Shell)
  if [[ -n "${GOOGLE_CLOUD_PROJECT}" ]]; then
    ENV_TYPE="cloud"
  # Option 2: Heuristic: check for known cloud-only files
  elif [[ -f "/.dockerenv" ]] || [[ -d "/workspace" ]]; then
    ENV_TYPE="cloud"
  else
    ENV_TYPE="local"
  fi

  echo "Detected environment type: $ENV_TYPE"
}

# List of required Linux packages (can add more per environment)
LINUX_PACKAGES=("curl" "git" "python3" "pipx")

setup_bashrc() {
  local os_dir
  os_dir="$(dirname "$0")"
  echo "Copying Linux bashrc templates..."

  # Always set up the local template
  cp "$os_dir/.bashrc.local.example" "$HOME/.bashrc.local"

  # If in cloud environment, also set up the cloud-specific template
  if [[ "$ENV_TYPE" == "cloud" ]]; then
    cp "$os_dir/.bashrc.cloud.example" "$HOME/.bashrc.cloud"
  fi
}

install_linux_packages() {
  echo "Installing Linux packages..."
  apt-get update -y
  apt-get install -y "${LINUX_PACKAGES[@]}"
}

# Detect environment type as soon as this script is sourced
detect_env_type
