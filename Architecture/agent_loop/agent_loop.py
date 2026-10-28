# agent loop

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Read configuration
model = os.getenv("MODEL")
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

messages = [
    {"role": "system", "content": "Your are an useful assistnat."}
]

questions = [
    "What is an agent?",
    "How is that different from a chatbot?",
    "Give me one example.",
]

for question in questions:
    messages.append({"role":"user", "content": question})
    while True:
        response = client.chat.completions.create(
            model = model,
            messages=messages
        )

        finish_reason = response.choices[0].finish_reason
        if finish_reason == "stop":
            reply = response.choices[0].message.content
            print(f"Q: {question}")
            print(f"A: {reply}")
            print()
            messages.append({"role": "assistant", "content": reply})
            break
        else:
            break