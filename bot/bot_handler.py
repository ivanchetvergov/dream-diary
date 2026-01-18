"""Telegram Bot Handler for DreamDiary AI."""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent import DreamDiaryAgent
from config import Config


class TelegramBotHandler:
    """Handles Telegram bot interactions."""

    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")
        self.agent = DreamDiaryAgent()
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up command and message handlers."""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_dream))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "Welcome to DreamDiary AI! Send me your dream text, and I'll analyze it with psychological insights. "
            "Use /help for more info."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "DreamDiary AI - Your personal dream analyst.\n\n"
            "Commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help\n\n"
            "Just send a dream description, and I'll provide analysis, emotions, and meditation suggestions."
        )
        await update.message.reply_text(help_text)

    async def handle_dream(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming dream text."""
        dream_text = update.message.text
        user_id = update.effective_user.id

        try:
            response = self.agent.process_dream(dream_text, user_id=user_id)
            await update.message.reply_text(response)
        except Exception as e:
            logging.error(f"Error processing dream: {e}")
            await update.message.reply_text("Sorry, an error occurred. Please try again.")

    def run(self):
        """Run the bot."""
        logging.info("Starting Telegram bot...")
        self.app.run_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = TelegramBotHandler()
    bot.run()
