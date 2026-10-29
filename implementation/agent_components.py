# Agent components
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# Read configuration from environment variables
model = os.getenv("MODEL")
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful personal assistant. Use your tools when you need real data."
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the user's calendar for events on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to check the calendar for events (format: YYYY-MM-DD)."
                    }
                },
                "required": ["date"],
            }
        }
    }
]

def check_calender(date):
    return "10am: Team standup, 2pm: Dentist appointment"


messages.append({"role": "user", "content": "What's on my calendar today?"})

while True:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    finish_reason = response.choices[0].finish_reason
    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    if finish_reason == "tool_calls":
        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if name == "check_calendar":
                result = check_calender(**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            }
            )

    elif finish_reason == "stop":
        print(assistant_message.content)
        break