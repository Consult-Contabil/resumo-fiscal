# Makefile for Resumo Fiscal Project
# A Flask application with Tailwind CSS

.PHONY: help install install-dev run dev build-css watch-css clean test lint format check deploy

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install Python dependencies using uv
	uv sync

install-dev: ## Install development dependencies
	uv sync --dev
	npm install

# Development
run: ## Run the Flask application
	python app.py

dev: ## Run the Flask application in development mode
	FLASK_ENV=development FLASK_DEBUG=1 python app.py

# CSS/Tailwind
build-css: ## Build Tailwind CSS
	npm run tailwind

watch-css: ## Watch and build Tailwind CSS in development mode
	npm run tailwind

# Testing and Quality
test: ## Run tests
	python -m pytest tests/ -v

lint: ## Run linting checks
	uv run ruff check .
	uv run ruff format --check .

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

check: ## Run all checks (lint, format, test)
	$(MAKE) lint
	$(MAKE) test

# Database
db-migrate: ## Run database migrations
	@echo "Database migrations not configured yet"

db-seed: ## Seed database with sample data
	@echo "Database seeding not configured yet"

# Cleaning
clean: ## Clean build artifacts and cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf build/
	rm -rf dist/

clean-css: ## Clean CSS build files
	rm -f static/output.css

clean-all: clean clean-css ## Clean all build artifacts

# Deployment
deploy: build-css ## Deploy to production
	@echo "Deploying to production..."
	@echo "Make sure to set up your deployment environment variables"

deploy-heroku: build-css ## Deploy to Heroku
	@echo "Deploying to Heroku..."
	git add .
	git commit -m "Deploy to Heroku"
	git push heroku main

# Docker
docker-build: ## Build Docker image
	docker build -t resumo-fiscal .

docker-run: ## Run Docker container
	docker run -p 5000:5000 resumo-fiscal

docker-stop: ## Stop Docker container
	docker stop $$(docker ps -q --filter ancestor=resumo-fiscal)

# Development setup
setup: install install-dev build-css ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make dev' to start the development server"

# Monitoring and logs
logs: ## Show application logs
	tail -f logs/app.log

# Backup
backup: ## Create backup of important files
	@echo "Creating backup..."
	tar -czf backup-$$(date +%Y%m%d-%H%M%S).tar.gz \
		--exclude='node_modules' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		--exclude='*.log' \
		.

# Security
security-check: ## Run security checks
	uv run safety check
	uv run bandit -r . -f json -o bandit-report.json

# Performance
profile: ## Profile the application
	uv run py-spy record -o profile.svg -- python app.py

# Documentation
docs: ## Generate documentation
	@echo "Documentation generation not configured yet"

# Database operations
db-backup: ## Backup database
	@echo "Database backup not configured yet"

db-restore: ## Restore database
	@echo "Database restore not configured yet"

# Environment
env-example: ## Create example environment file
	@echo "Creating .env.example..."
	@echo "# Flask Configuration" > .env.example
	@echo "FLASK_ENV=development" >> .env.example
	@echo "FLASK_DEBUG=1" >> .env.example
	@echo "PORT=5000" >> .env.example
	@echo "" >> .env.example
	@echo "# Database Configuration" >> .env.example
	@echo "DATABASE_URL=postgresql://user:password@localhost/resumo_fiscal" >> .env.example
	@echo "" >> .env.example
	@echo "# Security" >> .env.example
	@echo "SECRET_KEY=your-secret-key-here" >> .env.example

# Quick commands
quick-start: setup dev ## Quick start: setup and run development server

quick-deploy: build-css deploy ## Quick deploy: build CSS and deploy

# Development workflow
workflow: format lint test ## Run full development workflow (format, lint, test)

# Production preparation
prod-prep: clean build-css check ## Prepare for production (clean, build, check) 