# Resolusi-Pasha

Rencana kedepan Pasha — sekaligus jadi tempat ngumpulin proyek belajar.

## Telegram AI Chatbot

Bot Telegram sederhana yang mendukung **perintah dasar** + **chat ke AI**
(via API yang OpenAI-compatible: OpenAI, OpenRouter, DeepSeek, Groq, dll).

### Struktur

```
bot/
  __init__.py
  config.py     # load env vars
  ai.py         # client AI + memori per-user
  handlers.py   # /start, /help, /reset, /about, dan chat handler
  main.py       # entry point (long polling)
requirements.txt
.env.example
```

### Perintah bot

| Perintah | Fungsi                              |
|----------|-------------------------------------|
| `/start` | Tampilkan pesan sambutan + bantuan  |
| `/help`  | Sama seperti `/start`               |
| `/reset` | Hapus riwayat percakapan user       |
| `/about` | Info singkat tentang bot            |
| *(teks)* | Pesan biasa diteruskan ke AI        |

### Setup

1. **Buat bot di Telegram**
   - Chat ke [@BotFather](https://t.me/BotFather), jalankan `/newbot`,
     ikuti petunjuk, lalu salin token-nya.

2. **Siapkan API AI**
   - OpenAI: ambil key di <https://platform.openai.com/api-keys>.
   - Atau provider lain (OpenRouter / DeepSeek / Groq / dll) — cukup ganti
     `OPENAI_BASE_URL` dan `OPENAI_MODEL` di `.env`.

3. **Install dependency**
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Konfigurasi environment**
   ```bash
   cp .env.example .env
   # buka .env, isi TELEGRAM_BOT_TOKEN dan OPENAI_API_KEY
   ```

5. **Jalankan bot**
   ```bash
   python -m bot.main
   ```
   Buka Telegram, cari nama bot kamu, kirim `/start`.

### Catatan

- Riwayat percakapan disimpan di **memori proses** (akan hilang saat bot
  restart). Untuk produksi, ganti dict di `bot/ai.py` dengan storage
  persisten (SQLite/Redis/dll).
- Jangan commit file `.env` — sudah ada di `.gitignore`.
