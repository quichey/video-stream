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

# Safely update bashrc with variables from example file
BASHRC="$HOME/.bashrc"
EXAMPLE_FILE=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$DEPLOY_ENV" == "cloud" ]]; then
    EXAMPLE_FILE="$SCRIPT_DIR/bashrc.cloud.example"
else
    EXAMPLE_FILE="$SCRIPT_DIR/bashrc.local.example"
fi

echo "[env_setup] Updating $BASHRC using $EXAMPLE_FILE ..."

# Ensure DEPLOY_ENV is set explicitly
if ! grep -q "export DEPLOY_ENV=" "$BASHRC"; then
    echo "export DEPLOY_ENV=$DEPLOY_ENV" >> "$BASHRC"
fi

# Add $HOME/.local/bin to PATH if not already there
if ! grep -q "\$HOME/.local/bin" "$BASHRC"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$BASHRC"
fi

# Append only variables from example file that are not already present
if [[ -f "$EXAMPLE_FILE" ]]; then
    while IFS= read -r line; do
        # Ignore blank lines and comments
        if [[ -z "$line" || "$line" =~ ^# ]]; then
            continue
        fi
        # Extract the variable name
        var_name=$(echo "$line" | cut -d'=' -f1 | awk '{print $NF}' | sed 's/export //')
        # Check if that variable is already in ~/.bashrc
        if ! grep -q "$var_name" "$BASHRC"; then
            echo "$line" >> "$BASHRC"
        fi
    done < "$EXAMPLE_FILE"
fi

# Apply immediately for current session
echo "[env_setup] Applying updated bashrc..."
# shellcheck disable=SC1090
source "$BASHRC"

echo "[env_setup] Environment setup complete."
