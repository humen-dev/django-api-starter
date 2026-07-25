WEB := docker compose exec web

.PHONY: help build up down restart logs shell \
        migrate makemigrations createsuperuser djshell \
        lint format

help:
	@echo "Docker"
	@echo "  build            Build the Docker image"
	@echo "  up               Start all services (detached)"
	@echo "  down             Stop all services"
	@echo "  down-v           Stop all services and remove volumes"
	@echo "  restart          Restart the web service"
	@echo "  logs             Tail logs from all services"
	@echo "  shell            Open a bash shell in the web container"
	@echo ""
	@echo "Django"
	@echo "  migrate          Apply database migrations"
	@echo "  makemigrations   Create new migrations (use app=<name> to target an app)"
	@echo "  createsuperuser  Create a Django superuser"
	@echo "  djshell          Open the Django shell"
	@echo ""
	@echo "Ruff"
	@echo "  lint             Run ruff linter"
	@echo "  format           Run ruff formatter"

# Docker

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

restart:
	docker compose restart web

logs:
	docker compose logs -f

shell:
	$(WEB) bash

# Django

migrate:
	$(WEB) uv run python manage.py migrate

makemigrations:
	$(WEB) uv run python manage.py makemigrations $(app)

createsuperuser:
	$(WEB) uv run python manage.py createsuperuser

djshell:
	$(WEB) uv run python manage.py shell

# Ruff

lint:
	uv run ruff check .

format:
	uv run ruff format .
