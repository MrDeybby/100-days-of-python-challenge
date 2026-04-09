"""
Simple terminal chatbot that responds from a small Q&A bank.

Features:
- Loop for user input in the terminal.
- Looks for the closest matching question/keyword.
- Handles exit commands gracefully.
"""

from difflib import SequenceMatcher
from typing import Dict, List, Tuple


QNA_BANK: Dict[str, str] = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hello! Ask me anything or type 'exit' to leave.",
    "how are you": "I'm just code, but I'm running great—thanks!",
    "what is your name": "I'm a tiny terminal chatbot.",
    "help": "Try asking about time, name, or say hello. Type 'exit' to quit.",
    "time": "I don't have a clock, but it's always a good time to code.",
    "python": "Python is a versatile language great for automation and data.",
}

EXIT_WORDS = {"exit", "quit", "salir", "bye"}


def find_best_response(message: str) -> Tuple[str, float]:
    """
    Return the best matching response and its similarity score.
    Uses simple string similarity over the predefined Q&A bank.
    """
    message = message.lower().strip()
    best_key = None
    best_score = 0.0

    for key in QNA_BANK:
        score = SequenceMatcher(None, message, key).ratio()
        if score > best_score:
            best_key = key
            best_score = score

    if best_key is None:
        return "I didn't catch that. Can you rephrase?", 0.0
    return QNA_BANK[best_key], best_score


def main() -> None:
    print("Terminal Chatbot ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            print("Bot: Please type something so I can respond.")
            continue

        if user_input.lower() in EXIT_WORDS:
            print("Bot: Goodbye!")
            break

        response, score = find_best_response(user_input)
        if score < 0.45:
            response = (
                "Not sure I understood, but here's my best guess: "
                f"{response}"
            )
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
