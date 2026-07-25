# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Docker (local development)

```bash
cp .env.example .env   # create local env file (edit as needed)
make build             # build the Docker image
make up                # start web + postgres (detached)
make migrate           # apply migrations
make down              # stop; use make down-v to also delete the DB volume
```

Run `make help` to list all available targets. The `web` service mounts the project root as `/app`, so code changes are reflected immediately without a rebuild.

## Commands

**Package management** (uses `uv`, not pip):
```bash
uv add <package>          # Add a dependency
uv sync                   # Install all dependencies from uv.lock
uv run <command>          # Run a command in the project environment
```

**Django management**:
```bash
uv run python manage.py runserver         # Start dev server
uv run python manage.py migrate           # Apply migrations
uv run python manage.py makemigrations    # Create new migrations
uv run python manage.py createsuperuser   # Create admin user
uv run python manage.py startapp <name>   # Create a new Django app
```

**Running tests** (none configured yet — when added, likely):
```bash
uv run python manage.py test              # Django test runner
# or if pytest-django is added:
uv run pytest
```

## Architecture

**Stack:** Django 6.0.7, Python 3.14+, SQLite (dev), uv for dependency management.

The project lives in `contact_hub_api/` (the Django project package):
- `settings.py` — single settings file, `DEBUG=True`, SQLite database
- `urls.py` — root URL config; currently only the admin at `/admin/`
- `wsgi.py` / `asgi.py` — WSGI/ASGI entry points for deployment

**State:** This is a freshly scaffolded Django project. No custom apps, models, views, or tests exist yet. The intended domain is contact management (a "contact hub").

**No DRF installed.** If building a REST API, Django REST Framework will need to be added via `uv add djangorestframework` and registered in `INSTALLED_APPS`.

When creating new apps, register them in `INSTALLED_APPS` in `contact_hub_api/settings.py` and wire their URLs into `contact_hub_api/urls.py`.
