#!/usr/bin/env bash

ROOT_DIR="../../"

TARGET=$1

if [ "$TARGET" == "client" ]; then
  [ ! -f "${ROOT_DIR}client/.env" ] && cp "${ROOT_DIR}client/.env.example" "${ROOT_DIR}client/.env"
  echo "Copied ${ROOT_DIR}client/.env.example to ${ROOT_DIR}client/.env if missing."
  
  [ ! -f "${ROOT_DIR}client/env" ] && cp "${ROOT_DIR}client/.env" "${ROOT_DIR}client/env"
  echo "Copied ${ROOT_DIR}client/.env to ${ROOT_DIR}client/env if missing."

elif [ "$TARGET" == "server" ]; then
  [ ! -f "${ROOT_DIR}server/.env" ] && cp "${ROOT_DIR}server/.env.example" "${ROOT_DIR}server/.env"
  echo "Copied ${ROOT_DIR}server/.env.example to ${ROOT_DIR}server/.env if missing."
  
  [ ! -f "${ROOT_DIR}server/env" ] && cp "${ROOT_DIR}server/.env" "${ROOT_DIR}server/env"
  echo "Copied ${ROOT_DIR}server/.env to ${ROOT_DIR}server/env if missing."

else
  echo "Usage: $0 [client|server]"
  exit 1
fi
