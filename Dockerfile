FROM python:3.13-slim

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]
