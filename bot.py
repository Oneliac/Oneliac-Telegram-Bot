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
        self.app.add_handler(CommandHandler("eligibility", self.eligibility_command))
        self.app.add_handler(CommandHandler("prescription", self.prescription_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Healthcare Bot - Privacy-Preserving Medical Queries")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
Healthcare Bot Commands:
/start - Start the bot
/help - Show this help
/health - Check API status
/eligibility <patient_id> <procedure> - Check eligibility
/prescription <patient_id> <drug_code> - Validate prescription
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

    async def eligibility_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /eligibility <patient_id> <procedure_code>")
            return

        patient_id = context.args[0]
        procedure_code = context.args[1]

        try:
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "procedure_code": procedure_code
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/verify-eligibility",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("eligible"):
                            await update.message.reply_text(f"Patient {patient_id} is ELIGIBLE for {procedure_code}")
                        else:
                            await update.message.reply_text(f"Patient {patient_id} is NOT eligible")
                    else:
                        await update.message.reply_text("API Error")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def prescription_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /prescription <patient_id> <drug_code>")
            return

        patient_id = context.args[0]
        drug_code = context.args[1]

        try:
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "drug_code": drug_code
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/validate-prescription",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("valid"):
                            await update.message.reply_text(f"Prescription for {drug_code} is VALID")
                        else:
                            await update.message.reply_text(f"Prescription WARNING: {data.get('reason', 'Unknown')}")
                    else:
                        await update.message.reply_text("API Error")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    def run(self):
        logger.info("Starting Healthcare Bot...")
        self.app.run_polling()


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    bot = HealthcareBot(BOT_TOKEN, API_BASE_URL)
    bot.run()
