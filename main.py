
import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzMz4CQxeF9G2OwyZmv6Pwd1y6MMBChs96gWgrV--c1geSAWCeeZaRNJwclN326zgZd/exec"

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 7:
            await update.message.reply_text("❌ Формат: /log XAU/USD BUY 2350 2345 2365 1:3 Комментарий")
            return

        payload = {
            "asset": args[0],
            "orderType": args[1].upper(),
            "entry": float(args[2]),
            "sl": float(args[3]),
            "tp": float(args[4]),
            "rr": args[5],
            "comment": " ".join(args[6:]),
            "screenshot": ""
        }

        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            await update.message.reply_text("✅ Сделка записана в таблицу!")
        else:
            await update.message.reply_text("⚠️ Ошибка отправки в Google Sheets.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("log", log_command))
    app.run_polling()
