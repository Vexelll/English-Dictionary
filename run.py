from app import app
from telegram_bot.bot import main as bot_main
import multiprocessing
import time
import signal
import sys


def signal_handler(sig, frame):
    print('Завершение работы...')
    sys.exit(0)

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_bot():
    bot_main()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Создаем отдельные процессы
    flask_process = multiprocessing.Process(target=run_flask)
    bot_process = multiprocessing.Process(target=run_bot)
    
    # Запускаем процессы
    flask_process.start()
    bot_process.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        flask_process.terminate()
        bot_process.terminate()
        flask_process.join()
        bot_process.join()