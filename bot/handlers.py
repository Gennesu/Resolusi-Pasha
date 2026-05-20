"""Telegram update handlers."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from . import ai

logger = logging.getLogger(__name__)


WELCOME = (
    "Halo! Saya bot AI di Telegram.\n\n"
    "Perintah yang tersedia:\n"
    "/start  - Tampilkan pesan ini\n"
    "/help   - Bantuan\n"
    "/reset  - Hapus riwayat percakapan\n"
    "/about  - Tentang bot ini\n\n"
    "Kirim pesan teks apa pun untuk ngobrol dengan AI."
)

ABOUT = (
    "Bot Telegram + AI sederhana.\n"
    "Dibuat dengan python-telegram-bot dan OpenAI-compatible API."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(WELCOME)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(WELCOME)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return
    ai.reset(user.id)
    await update.message.reply_text("Riwayat percakapan dihapus.")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(ABOUT)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    user = update.effective_user
    if message is None or user is None or not message.text:
        return

    try:
        await context.bot.send_chat_action(
            chat_id=message.chat_id, action=ChatAction.TYPING
        )
    except Exception:  # pragma: no cover - non-fatal UX hint
        logger.debug("Failed to send typing action", exc_info=True)

    try:
        reply = await ai.chat(user.id, message.text)
    except Exception:
        logger.exception("AI request failed for user %s", user.id)
        await message.reply_text(
            "Maaf, terjadi kesalahan saat menghubungi AI. Coba lagi sebentar lagi."
        )
        return

    await message.reply_text(reply or "(Tidak ada balasan dari AI.)")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception while processing update", exc_info=context.error)
