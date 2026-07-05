# 🖥️ XStore — Pre-built Gaming PCs

Full-stack e-commerce built with Django. REST API + GraphQL, JWT auth, Docker production setup with Nginx & Gunicorn.

🌐 **Live:** https://store-fxui.onrender.com

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-informational)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6, Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| GraphQL | `graphene-django`, GraphiQL |
| Database | PostgreSQL 16 |
| Infrastructure | Docker Compose, Gunicorn, Nginx |
| Static files | `whitenoise` (production) |
| Package manager | `uv` |
| API docs | `drf-spectacular` (Swagger / OpenAPI) |
| Testing | `pytest-django` |

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
├── static/                  # source CSS files
│   └── css/
│       ├── base.css
│       ├── products.css
│       ├── orders.css
│       └── users.css
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
└── .env                     # not committed — see .env.example
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
| `DATABASE_URL` | `postgresql://...` | Overrides DB\_\* vars (used on Render) |
| `ALLOWED_HOSTS` | `localhost,yourdomain.com` | Comma-separated allowed hosts |

### 3. Run with Docker

```bash
docker compose up --build
```

On first start `entrypoint.sh` runs `migrate` and `collectstatic` automatically.

App available at `http://localhost` — served by Nginx → Gunicorn.

### 4. Seed sample products

```bash
docker compose exec web .venv/bin/python manage.py seed_products
```

### 5. Useful commands

```bash
# create admin account for /admin/ panel
docker compose exec web .venv/bin/python manage.py createsuperuser

# run tests
docker compose exec web .venv/bin/pytest

# lint + type check
docker compose exec web .venv/bin/flake8 .
docker compose exec web .venv/bin/mypy .
```

---

## Deploy on Render

1. Create a **PostgreSQL** database on Render → copy **Internal Database URL**
2. Create a **Web Service** → connect GitHub repo → runtime **Docker**
3. Set environment variables:

| Variable | Value |
|---|---|
| `SECRET_KEY` | your secret key |
| `DEBUG` | `False` |
| `DATABASE_URL` | Internal Database URL from Render PostgreSQL |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |

4. Pre-Deploy Command: `.venv/bin/python manage.py migrate`
5. Deploy — static files are served by `whitenoise`, no Nginx needed.

---

## REST API

Base URL: `/api/` — full interactive docs at `/api/docs/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/token/` | — | Obtain JWT access + refresh token |
| `POST` | `/api/token/refresh/` | — | Refresh access token |
| `POST` | `/api/users/register/` | — | Register new user |
| `GET/PUT` | `/api/users/profile/` | 🔐 JWT | Get / update profile |
| `GET` | `/api/products/` | — | Product list — search, filter, sort |
| `GET` | `/api/products/{id}/` | — | Product detail |
| `GET` | `/api/categories/` | — | Category list |
| `GET` | `/api/orders/` | 🔐 JWT | User's orders |

### JWT usage example

```bash
# 1. get token
curl -X POST https://store-fxui.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret"}'

# 2. use token in requests
curl https://store-fxui.onrender.com/api/orders/ \
  -H "Authorization: Bearer <access_token>"
```

---

## GraphQL

Endpoint: `/graphql/` — interactive GraphiQL IDE available in browser.

```graphql
# product list with filters
query {
  allProducts(search: "RTX", minPrice: 40000) {
    id
    name
    price
    category { name }
  }
}

# single product by slug
query {
  product(slug: "gaming-pc-rtx-5090-core-ultra9-285k-64gb") {
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
| `http://localhost/products/` | Product catalog |
| `http://localhost/orders/cart/` | Cart |
| `http://localhost/users/login/` | Login |
| `http://localhost/admin/` | Django admin panel |
| `http://localhost/api/docs/` | Swagger API documentation |
| `http://localhost/graphql/` | GraphiQL interface |
