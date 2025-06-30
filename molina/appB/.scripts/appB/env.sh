#!/bin/bash

DATABASE_ENV_FILE="./.docker/appB/env/.env.database"
BACKEND_ENV_FILE="./project/.env"

if [ ! -f "$DATABASE_ENV_FILE" ]; then
    mkdir -p "$(dirname "$DATABASE_ENV_FILE")"
    touch "$DATABASE_ENV_FILE"
fi

if [ ! -f "$BACKEND_ENV_FILE" ]; then
    mkdir -p "$(dirname "$BACKEND_ENV_FILE")"
    touch "$BACKEND_ENV_FILE"
fi

POSTGRES_USER="postgres"
POSTGRES_PASSWORD=$(date +%s%N | sha256sum | base64 | head -c 16)
POSTGRES_DB="app_a_db"
POSTGRES_HOST="app_a_network"
POSTGRES_PORT="5432"

{
    echo "POSTGRES_USER=$POSTGRES_USER"
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"
    echo "POSTGRES_DB=$POSTGRES_DB"
    echo "POSTGRES_HOST=$POSTGRES_HOST"
    echo "POSTGRES_PORT=$POSTGRES_PORT"
} > "$DATABASE_ENV_FILE"


{
    echo "DB_HOST=$POSTGRES_HOST"
    echo "DB_PORT=$POSTGRES_PORT"
    echo "DB_NAME=$POSTGRES_DB"
    echo "DB_USER=$POSTGRES_USER"
    echo "DB_PASS=$POSTGRES_PASSWORD"
} > "$BACKEND_ENV_FILE"