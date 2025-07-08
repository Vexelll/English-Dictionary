from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi! Send me words in format: "word - translation - example"')

def add_word(update, context):
    try:
        text = update.message.text
        parts = [part.strip() for part in text.split('-')]
        
        if len(parts) < 2:
            update.message.reply_text('Error! Use format: "word - translation - example"')
            return
        
        conn = sqlite3.connect('vocabulary.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO words (word, translation, example) VALUES (?, ?, ?)',
                      (parts[0], parts[1], parts[2] if len(parts) > 2 else None))
        conn.commit()
        conn.close()
        
        update.message.reply_text(f'Word "{parts[0]}" added to vocabulary!')
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text('Something went wrong. Try again.')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, add_word))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()