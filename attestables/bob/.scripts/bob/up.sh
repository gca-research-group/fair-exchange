POSTGRES_DATA_PATH=./.docker/bob/volumes/postgres/data

if [[ ! -d "$POSTGRES_DATA_PATH" ]]; then
  mkdir -p "$POSTGRES_DATA_PATH"
fi

docker compose -f ./.docker/bob/docker-compose.yml up -d --build

echo "Waiting for 5 seconds"
sleep 5

if [[ $(docker inspect --format='{{.State.Health.Status}}' bob_database) != "healthy" ]]; then
  docker compose -f ./.docker/bob/docker-compose.yml up -d --build
fi