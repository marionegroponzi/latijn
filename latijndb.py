import json
import random
import os


class latijn_db:
    """Class to handle the database operations for the Latijn questions."""

    def __init__(self):
        pass

    def load_json(self, filename: str):
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

    def start_for_chat_id(self, chat_id: int):
        """Start the bot for a specific chat ID."""
        if chat_id is None:
            print("No chat ID provided. Exiting.")
            return

        print(f"Starting bot for chat ID: {chat_id}")
        latijn = self.load_json("latijn.json")
        if latijn is None:
            return

        # Flatten the dictionary, ignoring the first level
        flattened = {}
        for outer in latijn.values():
            flattened.update(outer)
        latijn = flattened

        # write the merged dictionary as latijn_{chat_id}.json
        with open(f"latijn_{chat_id}.json", "w") as f:
            json.dump(latijn, f, indent=4)
        print(f"latijn_{chat_id}.json created successfully.")

    def get_new_question_for_chat_id(self, chat_id: int) -> tuple[str, list, int]:
        """Get a random question for the chat ID."""
        if chat_id is None:
            print("No chat ID provided. Exiting.")
            return None, None, 0
        print(f"Getting question for chat ID: {chat_id}")
        questions = self.load_json(f"latijn_{chat_id}.json")
        if questions is None or len(questions) == 0:
            print(
                f"No questions available for chat ID: {chat_id}. Please start the bot first."
            )
            return None, None, 0

        question = random.choice(list(questions.keys()))
        answers = questions[question]

        print(f"Question: {question}, Answer: {answers}")
        return question, answers, len(questions)

    def load_current_question_for_chat_id(self, chat_id: int) -> tuple[str, list]:
        """Load the current question for the chat ID."""
        try:
            with open(f"question_{chat_id}.json", "r") as f:
                q = json.load(f)
                answers = [s.strip().lower() for s in q.get("answers", [])]
                return q["question"].strip().lower(), answers
        except FileNotFoundError:
            print(f"No current question file found for chat ID: {chat_id}.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON for chat ID: {chat_id}.")

        return None, None

    def save_question_for_chat_id(self, chat_id: int, question: str, answers: list):
        """Save the current question for the chat ID."""
        if chat_id is None or question is None:
            print("Chat ID or question is None. Exiting.")
            return
        try:
            q = {
                "question": question,
                "answers": answers,
            }
            with open(f"question_{chat_id}.json", "w") as f:
                json.dump(q, f, indent=4)
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
