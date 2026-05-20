"""Entry point: start the Telegram bot with long polling.

Run with::

    python -m bot.main
"""
from __future__ import annotations

import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from . import config, handlers


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=logging.INFO,
    )
    # The httpx logger that python-telegram-bot uses is very chatty at INFO.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    config.validate()

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help_cmd))
    app.add_handler(CommandHandler("reset", handlers.reset))
    app.add_handler(CommandHandler("about", handlers.about))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.chat)
    )
    app.add_error_handler(handlers.error_handler)

    logging.info("Bot is starting (long polling)...")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
