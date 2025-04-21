import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# 🔐 API kalitlar
TELEGRAM_TOKEN = '7512558958:AAEfvh45gp7mIbsN5HfYpKEtquw6anDMbz0'  # bu yerga o'zingizning tokeningizni yozing
OPENAI_API_KEY = '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'      # OpenAI tokeningiz

openai.api_key = OPENAI_API_KEY

# 📋 Log sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🧠 AI javobi
async def get_ai_response(user_message):
    def call_openai():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return response['choices'][0]['message']['content']
    return await asyncio.to_thread(call_openai)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalomu alaykum! Men UZ GPTAI – O‘zbekcha sun’iy intellekt chatbotman.\n\nSavolingizni yozing:")

# Matnli xabarga javob
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🧠 Javob tayyorlanmoqda... ⏳")
    try:
        ai_response = await get_ai_response(user_message)
        await update.message.reply_text(ai_response)
    except Exception as e:
        await update.message.reply_text("❌ Xatolik: " + str(e))

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 UZ GPTAI bot ishga tushdi...")
    app.run_polling()
