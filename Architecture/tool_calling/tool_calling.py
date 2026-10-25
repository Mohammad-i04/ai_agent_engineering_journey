"""
Lab 0225 - Build a Tool-Calling App.

Demonstrates tool definition, execution, and result handling.
"""

from openai import OpenAI
import json
from datetime import date as _date


# 1. Configure the API client
model = "llama3.1:8b"
client=OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
    )
    
    
# 2. Define the assistant's behavior and current date
system_message = (
    "You are a helpful personal assistant. "
    f"Today's date is {_date.today().isoformat()}."
)

# 3. Describe the tool and its required arguments
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the user's calendar for events on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to check in YYYY-MM-DD format.",
                    }
                },
                "required": ["date"],
            },
        },
    }
]


# 4. Implement the tool (currently returns mock data)
def check_calendar(date):
    # Replace this with a real calendar lookup.
    return "10am: Team standup, 2pm: Dentist appointment"


# 5. Route tool calls to their implementations
def execute_tool(name, args):
    if name == "check_calendar":
        # Unpack the dictionary into keyword arguments.
        return check_calendar(**args)

    # Reject unknown tool names.
    return f"Unknown tool: {name}"


# 6. Initialize the conversation history
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "What's on my calendar today?"},
]


# 7. Send the first request to the model
response = client.chat.completions.create(
    model=model,  # Replace with a supported model.
    messages=messages,
    tools=tools,
)

# 8. Check how the model finished its response
finish_reason = response.choices[0].finish_reason
print(f"Finish reason: {finish_reason}")


# 9. Handle tool calls if requested
if finish_reason == "tool_calls":
    assistant_message = response.choices[0].message

    # Preserve the assistant's tool-call message.
    messages.append(assistant_message)

    # Process each requested tool.
    for tool_call in assistant_message.tool_calls:
        name = tool_call.function.name

        # Convert JSON arguments into a Python dictionary.
        args = json.loads(tool_call.function.arguments)

        # Execute the requested tool.
        result = execute_tool(name, args)

        # Send the tool result back into the conversation.
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    # 10. Ask the model to respond using the tool results.
    final_response = client.chat.completions.create(
        model=model,  # Use a supported model.
        messages=messages,
        tools=tools,
    )

    # Print the model's final response.
    print(final_response.choices[0].message.content)

else:
    # Print the response if no tool call was requested.
    print(response.choices[0].message.content)