.PHONY: help install dev test coverage clean docker-build docker-run lint format

help:
	@echo "SSF Transmitter - Available Commands:"
	@echo "  make install       Install production dependencies"
	@echo "  make dev          Install development dependencies"
	@echo "  make test         Run tests"
	@echo "  make coverage     Run tests with coverage report"
	@echo "  make lint         Run code linting"
	@echo "  make format       Format code"
	@echo "  make clean        Clean up generated files"
	@echo "  make docker-build Build Docker image"
	@echo "  make docker-run   Run Docker container"
	@echo "  make run-dev      Run development server"
	@echo "  make run-prod     Run production server"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest

coverage:
	pytest --cov=src/ssf_transmitter --cov-report=html --cov-report=term

lint:
	@echo "Linting Python files..."
	@command -v pylint >/dev/null 2>&1 && pylint src/ssf_transmitter || echo "pylint not installed"
	@command -v flake8 >/dev/null 2>&1 && flake8 src/ssf_transmitter || echo "flake8 not installed"

format:
	@echo "Formatting Python files..."
	@command -v black >/dev/null 2>&1 && black src/ssf_transmitter tests || echo "black not installed"
	@command -v isort >/dev/null 2>&1 && isort src/ssf_transmitter tests || echo "isort not installed"

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	rm -rf certs/*.pem

docker-build:
	docker build -t ssf-transmitter:latest .

docker-run:
	docker run -p 8080:8080 \
		-e ISSUER=http://localhost:8080 \
		-e OKTA_DOMAIN=https://your-org.okta.com \
		-e KEY_ID=transmitter-key-1 \
		ssf-transmitter:latest

run-dev:
	@bash scripts/dev.sh

run-prod:
	@bash scripts/start.sh
