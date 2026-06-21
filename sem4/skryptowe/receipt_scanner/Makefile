.PHONY: up down migrate test lint

up:
	docker compose up -d --build

down:
	docker compose down

migrate:
	docker compose exec backend alembic upgrade head

test:
	docker compose exec backend pytest -q

lint:
	docker compose exec backend python -m compileall app
