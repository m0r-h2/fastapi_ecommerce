uvicorn app.main:app --reload
docker-compose up --buld
docker-compose down -v

docker compose exec web alembic upgrade head