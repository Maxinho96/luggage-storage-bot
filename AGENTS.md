# Luggage Storage Bot — Agent Instructions

Telegram bot that monitors a cloud-based locker management system and sends real-time status updates to designated managers.

## Architecture

| File | Responsibility |
|------|---------------|
| [`src/luggage_storage_bot/bot.py`](src/luggage_storage_bot/bot.py) | Telegram bot setup, job queue, message formatting and delivery |
| [`src/luggage_storage_bot/promotec.py`](src/luggage_storage_bot/promotec.py) | Authentication and HTML scraping of `https://client.somee.com/` |

**Data flow**: `promotec.py` authenticates and scrapes locker state/revenue → `bot.py` compares against previous state → sends Telegram message only when state changes.

Global state in `bot.py` tracks previous locker state and revenue to detect changes:
```python
last_lockers_state: dict[int, bool] = {}
last_lockers_amount = None
```

## Commands

```bash
make install        # uv sync — install dependencies
make run            # run the bot
make check          # ruff format --check + ruff check (run before committing)
make format         # ruff format — auto-format code
make lint           # ruff check — lint only
make lock           # uv lock — lock dependencies
make update         # uv lock --upgrade — upgrade dependencies
```

The project uses `uv` for package management. Always use `uv` (not pip) to manage packages.

## Environment Variables

All required at runtime — no defaults:

| Variable | Purpose |
|----------|---------|
| `TOKEN` | Telegram bot token |
| `MAX_ID` | Telegram chat ID for Max |
| `ANNA_ID` | Telegram chat ID for Anna |
| `USER` | Username for `client.somee.com` |
| `PASSWORD` | Password for `client.somee.com` |

## Key Constraints

- **Python `~=3.9.0`** (3.9.x only) — do not use syntax or stdlib features from 3.10+.
- `python-telegram-bot==11.1.0` — old API; uses `Updater`/`JobQueue`, not the modern `Application` pattern.
- `promotec.py` handles a 3-step ASP.NET form auth flow (VIEWSTATE + EVENTVALIDATION tokens); changing the flow order will break authentication.
- Messages are in Italian (e.g., `"Stato locker aggiornato"`, `"Incassi aggiornati"`).
- Job interval is 5 minutes (`interval=60 * 5`).
