#!/usr/bin/env bash

# Copy .env examples to .env if they don't already exist
[ ! -f client/.env ] && cp client/.env.example client/.env
[ ! -f server/.env ] && cp server/.env.example server/.env

echo "Copied .env.example files to .env if missing."

# Copy .env examples to .env if they don't already exist
[ ! -f client/.env ] && cp client/.env client/env
[ ! -f server/.env ] && cp server/.env server/env

echo "Copied .env files to env if missing."
