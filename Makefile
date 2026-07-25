WEB      := docker compose exec web
WEB_PROD := docker compose -f docker-compose.prod.yml exec web

.PHONY: help build up down down-v restart logs shell \
        prod-build prod-up prod-down prod-logs \
        migrate makemigrations createsuperuser djshell \
        lint format

help:
	@echo "Docker (dev)"
	@echo "  build            Build the Docker image"
	@echo "  up               Start all services (detached)"
	@echo "  down             Stop all services"
	@echo "  down-v           Stop all services and remove volumes"
	@echo "  restart          Restart the web service"
	@echo "  logs             Tail logs from all services"
	@echo "  shell            Open a bash shell in the web container"
	@echo ""
	@echo "Docker (prod)"
	@echo "  prod-build       Build the production image"
	@echo "  prod-up          Start production services (detached)"
	@echo "  prod-down        Stop production services"
	@echo "  prod-logs        Tail production logs"
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

# Docker (dev)

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

# Docker (prod)

prod-build:
	docker compose -f docker-compose.prod.yml build

prod-up:
	docker compose -f docker-compose.prod.yml up -d

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

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
