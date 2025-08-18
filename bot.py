# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Telegram Bot for Privacy-Preserving Healthcare Agents
Provides secure medical queries through chat interface.
"""

import asyncio
import aiohttp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class HealthcareBot:
    def __init__(self, bot_token: str, api_base_url: str):
        self.bot_token = bot_token
        self.api_base_url = api_base_url.rstrip('/')
        self.app = Application.builder().token(bot_token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("health", self.health_check))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Healthcare Bot - Connecting to API...")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
Healthcare Bot Commands:
/start - Start the bot
/help - Show this help
/health - Check API status
        """
        await update.message.reply_text(help_text)

    async def health_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        await update.message.reply_text(f"API Status: {data.get('status', 'Unknown')}")
                    else:
                        await update.message.reply_text(f"API Error: Status {response.status}")
        except Exception as e:
            await update.message.reply_text(f"Connection Error: {str(e)}")

    def run(self):
        logger.info("Starting Healthcare Bot...")
        self.app.run_polling()


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    bot = HealthcareBot(BOT_TOKEN, API_BASE_URL)
    bot.run()
