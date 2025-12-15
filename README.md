# Oneliac Telegram Bot

Telegram bot interface for the privacy-preserving healthcare agents.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token_from_botfather"
export API_BASE_URL="https://oneliac-api.onrender.com"

# Run the bot
python bot.py
```

## Get Your Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the token and set it as `TELEGRAM_BOT_TOKEN`

## Deploy to Render

1. Push this repo to GitHub
2. Create a new **Background Worker** on Render
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN` - Your bot token (keep secret!)
   - `API_BASE_URL` - Your deployed API URL

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu |
| `/help` | Show help |
| `/health` | Check API status |
| `/eligibility <patient_id> <procedure>` | Check insurance eligibility |
| `/prescription <patient_id> <drug_code>` | Validate prescription |
| `/status` | System status dashboard |

## Architecture

```
User (Telegram) --> Telegram Bot (Render Worker) --> API (Render Web Service)
```

The bot communicates with the API via HTTP - they are completely decoupled.
