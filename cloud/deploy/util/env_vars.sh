#!/usr/bin/env bash

# Usage: ./script.sh client
#        ./script.sh server

TARGET=$1

if [ "$TARGET" == "client" ]; then
  [ ! -f client/.env ] && cp client/.env.example client/.env
  echo "Copied client/.env.example to client/.env if missing."
  
  [ ! -f client/env ] && cp client/.env client/env
  echo "Copied client/.env to client/env if missing."

elif [ "$TARGET" == "server" ]; then
  [ ! -f server/.env ] && cp server/.env.example server/.env
  echo "Copied server/.env.example to server/.env if missing."
  
  [ ! -f server/env ] && cp server/.env server/env
  echo "Copied server/.env to server/env if missing."

else
  echo "Usage: $0 [client|server]"
  exit 1
fi
