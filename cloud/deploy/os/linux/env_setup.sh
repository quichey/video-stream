#!/usr/bin/env bash
# Environment setup script for Linux
# Usage: source deploy/os/linux/env_setup.sh

set -eEuo pipefail

echo "[env_setup] Starting environment setup..."

# Detect if we're in cloud (GCP Cloud Shell) or local
if [[ "${CLOUD_SHELL:-}" == "true" ]] || [[ -n "${GOOGLE_CLOUD_PROJECT:-}" ]]; then
    DEPLOY_ENV="cloud"
    echo "[env_setup] Cloud environment detected."
else
    DEPLOY_ENV="local"
    echo "[env_setup] Local environment detected."
fi

# Update system packages
echo "[env_setup] Updating apt packages..."
sudo apt-get update -y

# Node.js & npm
if ! command -v node >/dev/null 2>&1; then
    echo "[env_setup] Installing Node.js and npm..."
    sudo apt-get install -y nodejs npm
else
    echo "[env_setup] Node.js already installed."
fi

# Python Poetry
if ! command -v poetry >/dev/null 2>&1; then
    echo "[env_setup] Installing Poetry..."
    pip install --upgrade pip
    pip install poetry
else
    echo "[env_setup] Poetry already installed."
fi

# Update bashrc
BASHRC="$HOME/.bashrc"
echo "[env_setup] Updating $BASHRC ..."
{
    echo ""
    echo "# Added by deploy/os/linux/env_setup.sh"
    echo "export DEPLOY_ENV=$DEPLOY_ENV"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
} >> "$BASHRC"

# Apply immediately
echo "[env_setup] Applying updated bashrc..."
# shellcheck disable=SC1090
source "$BASHRC"

echo "[env_setup] Environment setup complete."
