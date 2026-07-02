FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv sync

COPY . .

EXPOSE 8000

# gunicorn вместо runserver
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
