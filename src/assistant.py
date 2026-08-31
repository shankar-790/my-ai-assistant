"""
A simple command-line AI assistant powered by the Anthropic API.

Setup:
    1. pip install -r requirements.txt
    2. export ANTHROPIC_API_KEY="your-key-here"
    3. python src/assistant.py
"""

import os
import sys
from anthropic import Anthropic


SYSTEM_PROMPT = "You are a helpful, concise personal assistant."


def get_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: Set the ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def chat_loop() -> None:
    client = get_client()
    history = []

    print("My AI Assistant (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history,
        )

        reply_text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        print(f"Assistant: {reply_text}\n")

        history.append({"role": "assistant", "content": reply_text})


if __name__ == "__main__":
    chat_loop()
