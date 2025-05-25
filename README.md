# Faster API

**Faster API** is a Python CLI tool for scaffolding and managing **FastAPI** projects with a Django-inspired developer experience. It boosts productivity for large-scale projects by offering modular project structure, built-in user authentication, and out-of-the-box support for PostgreSQL via Docker.

## Features

- Django-like commands: `startproject`, `startapp`, `runserver`, `makemigrations`, `migrate`, `createsuperuser`
- Modular project/app structure for scalable codebases
- Preconfigured with:
  - SQLAlchemy
  - Pydantic Settings module
  - User, profile, and preference models
  - Auth endpoints (OAuth2, registration, token refresh)
- Integrated PostgreSQL dev server powered by Docker

## Installation

```bash
pip install tle-faster-api
```

## CLI Usage

```bash
fasterapi <command> [options]
```

### Commands

- `startproject <name> [--db_port <port>]`: Create a new FastAPI project
- `startapp <name>`: Create a new app within the project
- `runserver [--host <host>] [--port <port>]`: Launch the development server
- `makemigrations`: Generate a new Alembic migration
- `migrate`: Apply all migrations
- `createsuperuser`: Create an admin user interactively
- `dbup`: Start a local PostgreSQL container
- `dbdown`: Stop the database container
- `dbreset`: Remove the database container and volume

## Getting Started

```bash
fasterapi startproject myproject
cd myproject
cp .env.example .env
fasterapi dbup
fasterapi makemigrations
fasterapi migrate
fasterapi runserver
```

## Creating an App

```bash
fasterapi startapp blog
```

Then update:

- `alembic/env.py`:
  ```python
  import app.blog.models
  ```

- `app/core/routers/v1.py`:
  ```python
  from app.blog import views as blog_views
  api_router.include_router(blog_views.router, prefix="/blog", tags=["blog"])
  ```

## Creating a Superuser

```bash
fasterapi createsuperuser
```

## PostgreSQL Dev Database

Faster API includes a docker-compose file to spin up a local PostgreSQL instance:

```bash
fasterapi dbup     # Start DB
fasterapi dbdown   # Stop DB
fasterapi dbreset  # Destroy DB & volume
```

## License

MIT