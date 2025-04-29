import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Sahifadan tasodifiy savol olish
def get_random_question():
    url = "http://questions.chgk.info/random.html"
    response = requests.get(url)
    
    # Agar sahifa muvaffaqiyatli yuklangan bo'lsa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Savolni HTMLdan olish
        question = soup.find('div', class_='q-text').get_text(strip=True)
        
        # Savolni qaytarish
        return question
    else:
        return "Savolni olishda xatolik yuz berdi."

# /start komandasiga javob
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! Tasodifiy savol olish uchun /question buyrug'ini yozing.")

# /question komandasiga javob
def question(update: Update, context: CallbackContext):
    question = get_random_question()
    update.message.reply_text(question)

# Botni ishga tushurish
def main():
    # BotFather orqali olingan API token
    updater = Updater("8016701013:AAEvtQ2DpkYcDm2GJ81PODFgluHkHlr5X0I", use_context=True)
    dp = updater.dispatcher
    
    # Handlerlar qo'shish
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("question", question))
    
    # Botni ishga tushurish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
