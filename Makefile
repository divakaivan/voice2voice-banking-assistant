.PHONY: setup_backend backend setup_frontend frontend history_db help

help:
	@echo "Available targets:"
	@echo "  setup_backend   - Set up the backend environment and install dependencies"
	@echo "  backend         - Start the backend server"
	@echo "  test_backend    - Run backend tests"
	@echo "  setup_frontend  - Install frontend dependencies"
	@echo "  frontend        - Start the frontend development server"
	@echo "  test_frontend   - Run frontend tests"
	@echo "  history_db      - Start the database using Docker Compose"

setup_backend:
	cd src/backend && \
		uv init --python 3.12.8 && \
		source venv/bin/activate && \
		uv pip install -r pyproject.toml --all-extras && \
		uv lock

backend:
	uv run --env-file .env uvicorn src.backend.server:app \
		--host 0.0.0.0 \
		--port 8000 \
		--reload

test_backend:
	cd src/backend && uv run pytest

setup_frontend:
	cd src/frontend && npm install

frontend:
	cd src/frontend && npm start

test_frontend:
	cd src/frontend && npm run test

history_db:
	docker-compose up -d