import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os 
import aiohttp
from datetime import datetime, timedelta

token = os.environ.get('TELEGRAM')

def next_friday():
    today = datetime.now()
    days_until_friday = (4 - today.weekday() + 7) % 7
    if days_until_friday == 0:
        days_until_friday = 7
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday.date()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def cancha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    friday = next_friday()
    url = f'https://custom-llm-rs9d.onrender.com/cancha?day={friday}'
    async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    data = await response.text()
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=data)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Error al obtener la información")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6488342940:AAGa07Xk1IcZQOg9XjWjGie4VOQp689toO8').build()
    
    start_handler = CommandHandler('cancha', cancha)
    application.add_handler(start_handler)
    
    application.run_polling()