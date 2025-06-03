import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import random
import json
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


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


def start_for_chat_id(chat_id):
    """Start the bot for a specific chat ID."""
    if chat_id is None:
        print("No chat ID provided. Exiting.")
        return

    print(f"Starting bot for chat ID: {chat_id}")
    latijn = load_json("latijn.json")
    if latijn is None:
        return

    # merge the dictionary ignoring the first level
    d = {}
    for k in list(latijn.keys()):
        for k2 in list(latijn[k].keys()):
            d[k2] = latijn[k][k2]
    latijn = d

    # write the merged dictionary as latijn_{chat_id}.json
    with open(f"latijn_{chat_id}.json", "w") as f:
        json.dump(latijn, f, indent=4)
    print(f"latijn_{chat_id}.json created successfully.")


def get_new_question_for_chat_id(chat_id):
    """Get a random question for the chat ID."""
    if chat_id is None:
        print("No chat ID provided. Exiting.")
        return None
    print(f"Getting question for chat ID: {chat_id}")
    questions = load_json(f"latijn_{chat_id}.json")
    if questions is None or len(questions) == 0:
        print(
            f"No questions available for chat ID: {chat_id}. Please start the bot first."
        )
        return None

    keys = list(questions.keys())
    key_index = random.randint(0, len(keys) - 1)
    question = keys[key_index]
    answer = questions[question]
    print(f"Question: {question}, Answer: {answer}")
    return {"question": question, "answers": answer}


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_for_chat_id(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I've just reset your file, let's go!"
    )
    await ask_new_question(update, context)


def load_current_question_for_chat_id(chat_id):
    """Load the current question for the chat ID."""
    try:
        with open(f"question_{chat_id}.json", "r") as f:
            question_dict = json.load(f)
            return question_dict
    except FileNotFoundError:
        print(f"No current question file found for chat ID: {chat_id}.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON for chat ID: {chat_id}.")
        return None


def save_question_for_chat_id(chat_id, question):
    """Save the current question for the chat ID."""
    if chat_id is None or question is None:
        print("Chat ID or question is None. Exiting.")
        return
    try:
        with open(f"question_{chat_id}.json", "w") as f:
            json.dump(question, f, indent=4)
        print(f"Question saved for chat ID: {chat_id}.")
    except IOError as e:
        print(f"Error saving question for chat ID {chat_id}: {e}")


def remove_question_file_for_chat_id(chat_id):
    """Remove the current question file for the chat ID."""
    try:
        os.remove(f"question_{chat_id}.json")
        print(f"Removed question file for chat ID: {chat_id}.")
    except FileNotFoundError:
        print(f"No question file found for chat ID: {chat_id}.")
    except Exception as e:
        print(f"Error removing question file for chat ID {chat_id}: {e}")


def update_questions_list_for_chat_id(chat_id, question):
    """Update the questions list for the chat ID."""
    try:
        with open(f"latijn_{chat_id}.json", "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(f"No questions file found for chat ID: {chat_id}.")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON for chat ID: {chat_id}.")
        return

    if question in questions:
        del questions[question]
        with open(f"latijn_{chat_id}.json", "w") as f:
            json.dump(questions, f, indent=4)
        print(f"Updated questions list for chat ID: {chat_id}.")
    else:
        print(
            f"Question '{question}' not found in questions list for chat ID: {chat_id}."
        )


async def on_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if there is a file named question_{chat_id}.json, load it
    chat_id = update.effective_chat.id
    current_question = load_current_question_for_chat_id(chat_id)
    if current_question is not None:
        correct_answers = current_question.get("answers", [])
        if update.message.text in correct_answers:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Correct!"
            )
            update_questions_list_for_chat_id(chat_id, current_question["question"])
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Incorrect. {correct_answers}."
            )
        remove_question_file_for_chat_id(chat_id)

    # always ask anew question after answering
    await ask_new_question(update, context)


async def ask_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    new_question = get_new_question_for_chat_id(chat_id)
    if new_question is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No questions available. Please restart.",
        )
        return
    save_question_for_chat_id(chat_id, new_question)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=new_question["question"]
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(load_telegram_token()).build()

    start_handler = CommandHandler("start", on_start)
    application.add_handler(start_handler)

    question_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_question)
    application.add_handler(question_handler)

    application.run_polling()
