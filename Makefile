.PHONY: help install run-local test docker-build docker-up docker-down docker-logs clean

# Default target: show help
help:
	@echo "Available commands:"
	@echo "  make install        - Install python dependencies in the local virtual environment"
	@echo "  make run-local      - Run the app locally (outside Docker) using SQLite database"
	@echo "  make test           - Run automated integration tests locally"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Build and spin up the app and PostgreSQL database containers"
	@echo "  make docker-down    - Tear down running docker containers"
	@echo "  make docker-logs    - Follow docker container logs"
	@echo "  make clean          - Remove temporary files, SQLite DBs, and Python pycache"

# Install local dependencies
install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

# Run app locally (SQLite database default)
run-local:
	DB_HOST=localhost .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run local tests
test:
	.venv/bin/pip install httpx
	.venv/bin/python -m unittest test_app.py

# Docker: build images
docker-build:
	docker compose build

# Docker: spin up containers
docker-up:
	docker compose up -d

# Docker: tear down containers
docker-down:
	docker compose down -v

# Docker: tail logs
docker-logs:
	docker compose logs -f

# Clean temporary files
clean:
	rm -f library.db test_library.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
