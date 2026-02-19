# Modular Telegram Bot - Makefile
# =================================

.PHONY: help install run test clean lint format setup venv

# Default target
help:
	@echo "Modular Telegram Bot - Available Commands:"
	@echo "============================================"
	@echo "  make setup      - Setup development environment"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the bot"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter (flake8)"
	@echo "  make format     - Format code (black)"
	@echo "  make clean      - Clean cache and temp files"
	@echo "  make update     - Update dependencies"
	@echo "  make venv       - Create virtual environment"
	@echo "============================================"

# Setup development environment
setup: venv install
	@echo "✅ Setup complete!"
	@echo "📝 Please edit .env file with your BOT_TOKEN"
	@echo "🚀 Run 'make run' to start the bot"

# Create virtual environment
venv:
	@echo "🔄 Creating virtual environment..."
	python3 -m venv venv
	@echo "✅ Virtual environment created"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	venv/bin/pip install -U pip
	venv/bin/pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Run the bot
run:
	@echo "🚀 Starting bot..."
	venv/bin/python bot.py

# Run tests
test:
	@echo "🧪 Running tests..."
	@if command -v pytest >/dev/null 2>&1; then \
		venv/bin/pytest tests/ -v; \
	else \
		echo "⚠️  pytest not installed. Run 'make install-dev' first."; \
	fi

# Install dev dependencies
install-dev:
	@echo "📦 Installing dev dependencies..."
	venv/bin/pip install pytest pytest-asyncio black flake8 mypy
	@echo "✅ Dev dependencies installed"

# Run linter
lint:
	@echo "🔍 Running linter..."
	@if command -v flake8 >/dev/null 2>&1; then \
		venv/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
		venv/bin/flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics; \
	else \
		echo "⚠️  flake8 not installed. Run 'make install-dev' first."; \
	fi

# Format code
format:
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		venv/bin/black . --line-length 100; \
	else \
		echo "⚠️  black not installed. Run 'make install-dev' first."; \
	fi

# Type checking
typecheck:
	@echo "🔍 Running type checker..."
	@if command -v mypy >/dev/null 2>&1; then \
		venv/bin/mypy . --ignore-missing-imports; \
	else \
		echo "⚠️  mypy not installed. Run 'make install-dev' first."; \
	fi

# Update dependencies
update:
	@echo "🔄 Updating dependencies..."
	venv/bin/pip install -U -r requirements.txt
	@echo "✅ Dependencies updated"

# Clean cache and temp files
clean:
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	@echo "✅ Cleanup complete"

# Create necessary directories
init:
	@echo "📁 Creating directories..."
	mkdir -p data logs
	@echo "✅ Directories created"

# Backup database
backup:
	@echo "💾 Backing up database..."
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	cp data/bot_database.db "data/backup_$$timestamp.db" 2>/dev/null || echo "⚠️  No database to backup"; \
	@echo "✅ Backup created"

# Show logs
logs:
	@echo "📋 Showing logs..."
	@tail -f logs/bot.log 2>/dev/null || echo "⚠️  No log file found"

# Check environment
check:
	@echo "🔍 Checking environment..."
	@echo "Python version:"
	@python3 --version
	@echo ""
	@echo "Virtual environment:"
	@if [ -d "venv" ]; then echo "✅ venv exists"; else echo "❌ venv not found"; fi
	@echo ""
	@echo ".env file:"
	@if [ -f ".env" ]; then echo "✅ .env exists"; else echo "❌ .env not found"; fi
	@echo ""
	@echo "Dependencies:"
	@if [ -d "venv" ]; then \
		venv/bin/pip list 2>/dev/null | grep -E "(python-telegram-bot|python-dotenv)" || echo "⚠️  Some dependencies not found"; \
	else \
		echo "❌ venv not found"; \
	fi

# Full check before commit
check-all: lint typecheck test
	@echo "✅ All checks passed!"

# Quick start (setup + run)
quickstart: setup
	@echo "🚀 Quick start..."
	@echo "📝 Please edit .env file first, then run 'make run'"
