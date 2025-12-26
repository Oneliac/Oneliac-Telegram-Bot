# AGENTS.md - Oneliac Telegram Bot

## Commands
- **Run bot:** `python bot.py`
- **Install deps:** `pip install -r requirements.txt`
- **No tests currently** - consider adding pytest for unit tests

## Architecture
Single-file Python Telegram bot (`bot.py`) using `python-telegram-bot` async library.
- `HealthcareBot` class: main bot logic with command/message handlers
- Communicates with external API at `API_BASE_URL` via `aiohttp`
- Deployed as Render background worker (see `render.yaml`)

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather (required)
- `API_BASE_URL` - Backend API URL (default: https://oneliac-api.onrender.com)

## Code Style
- Python 3.10+, async/await patterns throughout
- Type hints: use `typing` module (Dict, Any, etc.)
- Logging via `logging` module, not print statements
- Markdown formatting in bot messages (parse_mode='Markdown')
- Error handling: try/except with user-friendly error messages
- Keep API calls in async context managers (`async with aiohttp.ClientSession()`)
