import json
import random
import os


class latijn_db:
    """Class to handle the database operations for the Latijn questions."""

    def __init__(self):
        pass

    def load_json(self, filename):
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

    def start_for_chat_id(self, chat_id):
        """Start the bot for a specific chat ID."""
        if chat_id is None:
            print("No chat ID provided. Exiting.")
            return

        print(f"Starting bot for chat ID: {chat_id}")
        latijn = self.load_json("latijn.json")
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

    def get_new_question_for_chat_id(self, chat_id):
        """Get a random question for the chat ID."""
        if chat_id is None:
            print("No chat ID provided. Exiting.")
            return None
        print(f"Getting question for chat ID: {chat_id}")
        questions = self.load_json(f"latijn_{chat_id}.json")
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

    def load_current_question_for_chat_id(self, chat_id):
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

    def save_question_for_chat_id(self, chat_id, question):
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

    def remove_question_file_for_chat_id(self, chat_id):
        """Remove the current question file for the chat ID."""
        try:
            os.remove(f"question_{chat_id}.json")
            print(f"Removed question file for chat ID: {chat_id}.")
        except FileNotFoundError:
            print(f"No question file found for chat ID: {chat_id}.")
        except Exception as e:
            print(f"Error removing question file for chat ID {chat_id}: {e}")

    def update_questions_list_for_chat_id(self, chat_id, question):
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
