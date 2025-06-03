POSTGRES_DATA_PATH=./.docker/appB/volumes/postgres/data

if [[ ! -d "$POSTGRES_DATA_PATH" ]]; then
  mkdir -p "$POSTGRES_DATA_PATH"
fi

docker compose -f ./.docker/appB/docker-compose.yml up -d --build

echo "Waiting for 5 seconds"
sleep 5

if [[ $(docker inspect --format='{{.State.Health.Status}}' app_b_database) != "healthy" ]]; then
  docker compose -f ./.docker/appB/docker-compose.yml up -d --build
fi