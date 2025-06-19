import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from bot_config import IS_PRODUCTION
from latijndb import latijn_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Latijn:
    """Class to handle the Latijn bot operations."""

    def __init__(self):
        self.latijn_db = latijn_db()
        self.application = (
            ApplicationBuilder().token(self.load_telegram_token()).build()
        )

        start_handler = CommandHandler("start", self.on_start)
        self.application.add_handler(start_handler)

        question_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.on_question
        )
        self.application.add_handler(question_handler)

        self.application.run_polling()

    async def on_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.latijn_db.start_for_chat_id(update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I've just reset your file, let's go!",
        )
        await self.ask_new_question(update, context)

    async def on_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        current_question = self.latijn_db.load_current_question_for_chat_id(chat_id)
        if current_question is not None:
            good_answers = [s.strip().lower() for s in current_question.get("answers", [])]
            user_answer = update.message.text.strip().lower()

            if user_answer in good_answers:
                await context.bot.send_message(
                    chat_id=chat_id, text="Correct!"
                )
                self.latijn_db.update_questions_list_for_chat_id(
                    chat_id, current_question["question"]
                )
            else:
                first_letter = good_answers[0][0]
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Incorrect. (the correct answer starts with {first_letter} ;)).",
                )
            self.latijn_db.remove_question_file_for_chat_id(chat_id)

        # always ask a new question after answering
        await self.ask_new_question(update, context)

    @staticmethod
    def load_telegram_token():
        try:
            import telegram_token

            token = telegram_token.telegram_token(IS_PRODUCTION)
            print("Telegram token loaded successfully.")
            return token
        except ImportError:
            print("telegram_token module not found. Exiting.")
            return None

    async def ask_new_question(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        chat_id = update.effective_chat.id
        new_question = self.latijn_db.get_new_question_for_chat_id(chat_id)
        if new_question is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No questions available. Please restart.",
            )
            return
        self.latijn_db.save_question_for_chat_id(chat_id, new_question)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=new_question["question"]
        )


if __name__ == "__main__":
    latijn = Latijn()
