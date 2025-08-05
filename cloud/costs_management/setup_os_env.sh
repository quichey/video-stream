#!/bin/bash

# Path to the cost management env file
ENV_FILE="$HOME/.bashrc.cost_management"
BASHRC_FILE="$HOME/.bashrc"

# Create the env file with dummy secure variables (replace with real secrets securely)
cat <<EOL > "$ENV_FILE"
# Azure Cost Management API Environment Variables
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_BILLING_ACCOUNT_ID="your-billing-account-id"
EOL

chmod 600 "$ENV_FILE"  # Restrict permissions

# Append sourcing line to .bashrc if not already present
if ! grep -qF "source ~/.bashrc.cost_management" "$BASHRC_FILE"; then
  echo -e "\n# Load Azure Cost Management environment variables" >> "$BASHRC_FILE"
  echo "source ~/.bashrc.cost_management" >> "$BASHRC_FILE"
fi

echo "Environment setup complete. Please run:"
echo "  source ~/.bashrc"
echo "or restart your terminal to apply changes."
