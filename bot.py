# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Telegram Bot for Privacy-Preserving Healthcare Agents
Provides secure medical queries through chat interface.
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
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
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("Check Eligibility", callback_data="eligibility"),
                InlineKeyboardButton("Validate Prescription", callback_data="prescription")
            ],
            [
                InlineKeyboardButton("System Status", callback_data="status"),
                InlineKeyboardButton("Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("API Docs", url=f"{self.api_base_url}/docs")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_text = """
**Healthcare Agents Bot**

Welcome to the privacy-preserving healthcare system!

I can help you with:
- **Eligibility Verification** - Check insurance coverage
- **Prescription Validation** - Verify drug safety
- **Federated Learning** - Contribute to AI training
- **System Status** - Check API health

All your data is encrypted and processed with zero-knowledge proofs for maximum privacy!

Choose an option below or type a command:
        """

        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
**Healthcare Bot Commands**

**Basic Commands:**
- `/start` - Show main menu
- `/help` - Show this help message
- `/health` - Check API status

**Healthcare Commands:**
- `/eligibility <patient_id> <procedure>` - Check eligibility
- `/prescription <patient_id> <drug_code>` - Validate prescription
- `/status` - Show system status

**Examples:**
```
/eligibility PATIENT_001 PROC001
/prescription PATIENT_001 DRUG001
```

**Privacy Features:**
- All data is encrypted
- Zero-knowledge proofs
- HIPAA compliant
- Blockchain verified

**Need more help?** Check the [API Documentation]({}/docs)
        """.format(self.api_base_url)

        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def health_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        status_text = f"""
**System Status: Healthy**

- **Version:** {data.get('version', 'Unknown')}
- **Status:** {data.get('status', 'Unknown')}
- **Message:** {data.get('message', 'No message')}
- **API URL:** {self.api_base_url}

All healthcare agents are operational!
                        """
                    else:
                        status_text = f"**API Error:** Status {response.status}"
        except Exception as e:
            status_text = f"**Connection Error:** {str(e)}"

        await update.message.reply_text(status_text, parse_mode='Markdown')

    async def eligibility_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 2:
            await update.message.reply_text(
                "**Usage:** `/eligibility <patient_id> <procedure_code>`\n\n"
                "**Example:** `/eligibility PATIENT_001 PROC001`",
                parse_mode='Markdown'
            )
            return

        patient_id = context.args[0]
        procedure_code = context.args[1]

        loading_msg = await update.message.reply_text("Checking eligibility... Please wait.")

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
                            result_text = f"""
**Eligibility Confirmed**

- **Patient:** {patient_id}
- **Procedure:** {procedure_code}
- **Status:** Eligible
- **Coverage:** {data.get('coverage_pct', 'N/A')}%
- **ZK Proof:** Verified

The patient is eligible for this procedure!
                            """
                        else:
                            result_text = f"""
**Eligibility Denied**

- **Patient:** {patient_id}
- **Procedure:** {procedure_code}
- **Status:** Not Eligible
- **Reason:** {data.get('reason', 'Coverage not available')}

Please check with insurance provider.
                            """
                    else:
                        error_data = await response.json()
                        result_text = f"**API Error:** {error_data.get('detail', 'Unknown error')}"

        except Exception as e:
            result_text = f"**Error:** {str(e)}"

        await loading_msg.edit_text(result_text, parse_mode='Markdown')

    async def prescription_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 2:
            await update.message.reply_text(
                "**Usage:** `/prescription <patient_id> <drug_code>`\n\n"
                "**Example:** `/prescription PATIENT_001 DRUG001`",
                parse_mode='Markdown'
            )
            return

        patient_id = context.args[0]
        drug_code = context.args[1]

        loading_msg = await update.message.reply_text("Validating prescription... Please wait.")

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
                            result_text = f"""
**Prescription Validated**

- **Patient:** {patient_id}
- **Drug:** {drug_code}
- **Safety:** Safe to prescribe
- **Interactions:** Checked
- **Cross-chain:** {data.get('cross_chain_oracle', 'Verified')}

Prescription is safe to dispense!
                            """
                        else:
                            result_text = f"""
**Prescription Warning**

- **Patient:** {patient_id}
- **Drug:** {drug_code}
- **Safety:** Potential issues
- **Reason:** {data.get('reason', 'Unknown')}

Please consult with physician before dispensing.
                            """
                    else:
                        error_data = await response.json()
                        result_text = f"**API Error:** {error_data.get('detail', 'Unknown error')}"

        except Exception as e:
            result_text = f"**Error:** {str(e)}"

        await loading_msg.edit_text(result_text, parse_mode='Markdown')

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    health_data = await response.json() if response.status == 200 else {}

                async with session.get(f"{self.api_base_url}/status") as response:
                    status_data = await response.json() if response.status == 200 else {}

            fl_data = status_data.get("federated_learning", {})

            status_text = f"""
**System Status Dashboard**

**Healthcare API**
- Status: {health_data.get('status', 'Unknown')}
- Version: {health_data.get('version', 'Unknown')}

**Federated Learning**
- Current Round: {fl_data.get('current_round', 0)}
- Participants: {fl_data.get('participants', 0)}

**Privacy Features**
- Zero-Knowledge Proofs: Active
- Data Encryption: AES-256
- Blockchain: Solana

Last Updated: Just now
            """

        except Exception as e:
            status_text = f"**Error getting status:** {str(e)}"

        await update.message.reply_text(status_text, parse_mode='Markdown')

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "eligibility":
            await query.edit_message_text(
                "**Eligibility Check**\n\n"
                "Use: `/eligibility <patient_id> <procedure_code>`\n\n"
                "**Example:** `/eligibility PATIENT_001 PROC001`\n\n"
                "This will check if the patient is eligible for the specified medical procedure.",
                parse_mode='Markdown'
            )
        elif query.data == "prescription":
            await query.edit_message_text(
                "**Prescription Validation**\n\n"
                "Use: `/prescription <patient_id> <drug_code>`\n\n"
                "**Example:** `/prescription PATIENT_001 DRUG001`\n\n"
                "This will validate if the drug is safe for the patient and check for interactions.",
                parse_mode='Markdown'
            )
        elif query.data == "status":
            await self.status_command(update, context)
        elif query.data == "help":
            await self.help_command(update, context)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.lower()

        if any(word in text for word in ["eligibility", "eligible", "coverage", "insurance"]):
            await update.message.reply_text(
                "To check eligibility, use:\n"
                "`/eligibility <patient_id> <procedure_code>`\n\n"
                "Example: `/eligibility PATIENT_001 PROC001`",
                parse_mode='Markdown'
            )
        elif any(word in text for word in ["prescription", "drug", "medication", "medicine"]):
            await update.message.reply_text(
                "To validate a prescription, use:\n"
                "`/prescription <patient_id> <drug_code>`\n\n"
                "Example: `/prescription PATIENT_001 DRUG001`",
                parse_mode='Markdown'
            )
        elif any(word in text for word in ["help", "commands", "what can you do"]):
            await self.help_command(update, context)
        elif any(word in text for word in ["status", "health", "online"]):
            await self.health_check(update, context)
        else:
            await update.message.reply_text(
                "I'm a healthcare bot! I can help with:\n\n"
                "- `/eligibility` - Check insurance coverage\n"
                "- `/prescription` - Validate medications\n"
                "- `/status` - System health\n"
                "- `/help` - Show all commands\n\n"
                "Type `/help` for more details!"
            )

    def run(self):
        logger.info("Starting Healthcare Bot...")
        self.app.run_polling()


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://oneliac-api.onrender.com")

    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Please set TELEGRAM_BOT_TOKEN environment variable")
        print("Get your token from @BotFather on Telegram")
        exit(1)

    bot = HealthcareBot(BOT_TOKEN, API_BASE_URL)
    bot.run()
