import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# 🔐 API kalitlar
TELEGRAM_TOKEN = '7512558958:AAEfvh45gp7mIbsN5HfYpKEtquw6anDMbz0'  # bu yerga o'zingizning tokeningizni yozing
OPENAI_API_KEY = '7355234094:AAGNISiLPtzjsE1DbQPJQEunp_xNH8fbJ5w'      # OpenAI tokeningiz
CHANNELS = ['@K_Kutubxonasi', '@SamurayHikmatlari']  # kerakli kanallar

openai.api_key = OPENAI_API_KEY

# 📋 Log sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Kanalga obuna bo‘lganini tekshirish
async def is_subscribed(user_id, context: ContextTypes.DEFAULT_TYPE):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

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
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        msg = "⛔️ Botdan foydalanishdan oldin quyidagi kanallarga obuna bo‘ling:\n\n"
        for ch in CHANNELS:
            msg += f"👉 {ch}\n"
        msg += "\n✅ Obuna bo‘lgach, qayta /start ni bosing."
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("👋 Assalomu alaykum! Men UZ GPTAI – O‘zbekcha sun’iy intellekt chatbotman.\n\nSavolingizni yozing:")

# Matnli xabarga javob
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        await start(update, context)
        return

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
