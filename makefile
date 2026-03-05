.PHONY: dev celery lint-check lint-fix dev-lint-check dev-lint-fix

dev:
	uv run uvicorn app.main:app --reload --port 8001

celery:
	uv run watchfiles --filter python "uv run celery -A app.celery worker --loglevel=info --pool=solo" app

lint-check:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix
	uv run ruff format .

dev-lint-check: lint-check

dev-lint-fix: lint-fix
