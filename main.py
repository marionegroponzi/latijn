import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random
import json

def load_json(filename):
    try:
        with open(filename, "r") as f:
            latijn = json.load(f)
    except FileNotFoundError:
        print("latijn.json not found. Please ensure the file exists.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from latijn.json.")
        return
    return latijn

def load_telegram_token():
    try:
        import telegram_token
        token = telegram_token.telegram_token()
        print("Telegram token loaded successfully.")
        return token
    except ImportError:
        print("telegram_token module not found. Exiting.")
        return None
    

# async def main():
#     print("Hello from latijn!")
#     # if the certificate.py file exists, import it and run the code
#     try:
#         import telegram_token
#         token = telegram_token.telegram_token()
#         print("Telegram token loaded successfully.")
#     except ImportError:
#         print("Certificate module not found. Exiting.")
#         return
    
#     bot = telegram.Bot(token)

#     async with bot:
#         print(await bot.get_me())
    

    # latijn = load_json("latijn.json")
    # if latijn is None:
    #     return
    
    # # merge the dictionary ignoring the first level
    # d = {}
    # for k in list(latijn.keys()):
    #     for k2 in list(latijn[k].keys()):
    #         d[k2] = latijn[k][k2]
        
    # latijn = d

    # while True:
    #     e = random.randint(0, len(latijn) - 1)
    #     k = list(latijn.keys())
    #     my_answer = input(k[e]+ ": ").lower()
    #     if my_answer in latijn[k[e]]:
    #         print("Correct!")
    #         latijn.pop(k[e])
    #     else:
    #         print("Incorrect!", latijn[k[e]])


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(load_telegram_token()).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
