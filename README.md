# XStore: Full-Stack E-Commerce Platform

🌐 **Live:** https://store-fxui.onrender.com

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-informational)

## Overview

An educational Django project demonstrating a complete online storefront for pre-built gaming PCs and smartphones. The application provides a server-rendered web interface and a REST API, both operating against shared domain models.

## Core Architecture

The platform implements two distinct access patterns:

- **Web storefront** using session-based authentication with server-rendered templates
- **REST API** utilizing JWT authentication for programmatic access
- **GraphQL endpoint** for flexible data queries with filtering support

## Key Technical Highlights

**Stack:**
- Django 6 with Python 3.13
- PostgreSQL 16 for persistence
- Docker Compose with Nginx + Gunicorn for local production setup
- Django REST Framework with JWT token management
- GraphQL via `graphene-django` with GraphiQL interface
- Whitenoise for static file serving in production

**Notable Features:**
- Transaction-safe checkout with atomic database operations to prevent overselling
- Price snapshots captured at order time — stored independently of current product price
- Session-based shopping cart requiring no authentication to browse
- Review system restricted to verified buyers — users can only review products they have purchased
- Modular CSS architecture with per-app stylesheets served via collectstatic pipeline

## Data Integrity & Business Logic

The checkout process operates within atomic transactions, ensuring stock is decremented and order items are created as a single unit of work. If any step fails, the entire operation rolls back. Product prices are saved directly to `OrderItem` at the moment of purchase, making order history immune to future price changes.

## API

The REST API is documented interactively at `/api/docs/` via Swagger UI. Public endpoints cover the product catalog and registration. Order management and profile access require JWT authentication passed as a Bearer token.

The GraphQL endpoint at `/graphql/` exposes products and categories with full filtering support — by search term, category slug, and price range.

## Quality Assurance

The project includes a pytest test suite covering catalog browsing, cart operations, checkout flow, and JWT authentication. Tests use dedicated fixtures and run against an isolated test database.

## Local Setup

```bash
git clone https://github.com/your-username/store.git
cd store
cp .env.example .env   # fill in your values
docker compose up --build
```

On first start, `entrypoint.sh` automatically runs migrations and collects static files. The application is available at `http://localhost`.

**Seed sample data:**
```bash
docker compose exec web .venv/bin/python manage.py seed_products
docker compose exec web .venv/bin/python manage.py createsuperuser
```

**Environment variables:**

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` | PostgreSQL credentials |
| `DATABASE_URL` | Overrides individual DB vars — used on Render |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |

## Deployment

The project is deployed on Render using the Docker runtime. Static files are served by Whitenoise — no separate Nginx required in the cloud environment. The database runs as a managed Render PostgreSQL instance connected via `DATABASE_URL`.
