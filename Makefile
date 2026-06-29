install:
	uv sync

run:
	uv run python src/luggage_storage_bot/bot.py

lock:
	uv lock

update:
	uv lock --upgrade

format:
	uv run ruff format

format-check:
	uv run ruff format --check

lint:
	uv run ruff check

check: format-check lint