.PHONY: up down logs migrate test shell

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f bot

migrate:
	docker compose exec bot alembic upgrade head

test:
	docker compose exec bot pytest

shell:
	docker compose exec bot /bin/bash
