# 🖥️ Store — PC Components Shop

Full-stack e-commerce built with Django. REST API + GraphQL, JWT auth, Docker production setup with Nginx & Gunicorn.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-informational)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5, Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| GraphQL | `graphene-django`, GraphiQL |
| Database | PostgreSQL 16 |
| Infrastructure | Docker Compose, Gunicorn, Nginx |
| Package manager | `uv` |
| API docs | `drf-spectacular` (Swagger / OpenAPI) |
| Testing | `pytest-django` |
| Linting | `flake8`, `mypy` |

---

## Project Structure

```
Store/
│
├── config/                  # project config
│   ├── settings.py
│   ├── urls.py
│   ├── api_urls.py          # REST API routes
│   └── ql_schema.py         # GraphQL root schema
│
├── products/                # catalog app
├── orders/                  # cart + checkout
├── reviews/                 # product reviews
├── users/                   # auth + profile
│
├── templates/               # HTML templates
│   └── base.html
│
├── tests/                   # pytest test suite
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_orders.py
│   └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── nginx.conf
└── .env                     # not committed
```

---

## Quick Start

### 1. Clone & configure environment

```bash
git clone https://github.com/your-username/store.git
cd store
cp .env.example .env   # fill in your values
```

### 2. Environment variables

| Variable | Example | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Django secret key |
| `DEBUG` | `False` | Set `True` in development only |
| `DB_NAME` | `store` | PostgreSQL database name |
| `DB_USER` | `store` | PostgreSQL user |
| `DB_PASSWORD` | `store` | PostgreSQL password |
| `DB_HOST` | `db` | Service name from docker-compose |
| `DB_PORT` | `5432` | PostgreSQL port |

### 3. Run with Docker

```bash
docker compose up --build
```

On first start `entrypoint.sh` runs `migrate` and `collectstatic` automatically.

App available at `http://localhost` — served by Nginx → Gunicorn.

### 4. Useful commands

```bash
# create admin account for /admin/ panel
docker compose exec web uv run python manage.py createsuperuser

# run tests
uv run pytest

# lint + type check
uv run flake8 . && uv run mypy .
```

---

## REST API

Base URL: `/api/` — full interactive docs at `/api/docs/`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/token/` | Obtain JWT access + refresh token |
| `POST` | `/api/token/refresh/` | Refresh access token |
| `POST` | `/api/users/register/` | Register new user |
| `GET` | `/api/users/profile/` | Get / update profile — 🔐 JWT |
| `GET` | `/api/products/` | Product list — search, filter, sort |
| `GET` | `/api/products/{id}/` | Product detail |
| `GET` | `/api/categories/` | Category list |
| `GET` | `/api/orders/` | User's orders — 🔐 JWT |
| `GET` | `/api/products/{id}/reviews/` | Reviews for a product |
| `POST` | `/api/products/{id}/reviews/` | Add review — 🔐 JWT |

### JWT usage example

```bash
# 1. get token
curl -X POST /api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret"}'

# 2. use token in requests
curl /api/orders/ \
  -H "Authorization: Bearer <access_token>"
```

---

## GraphQL

Endpoint: `/graphql/` — interactive GraphiQL IDE available in browser.

```graphql
# product list with filters
query {
  allProducts(search: "Ryzen", minPrice: 5000, categorySlug: "processors") {
    id
    name
    price
    category { name }
  }
}

# single product by slug
query {
  product(slug: "amd-ryzen-5-5600x") {
    name
    price
    stock
    category { name slug }
  }
}
```

---

## Available URLs

| URL | Description |
|---|---|
| `http://localhost/` | Site homepage |
| `http://localhost/admin/` | Django admin panel |
| `http://localhost/api/docs/` | Swagger API documentation |
| `http://localhost/graphql/` | GraphiQL interface |
