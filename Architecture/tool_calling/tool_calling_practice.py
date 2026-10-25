# calculate_sum program
# 1. Start the program.

from openai import OpenAI
import json

# 2. Prepair the API client and model configuration
model = "llama3.1:8b"
client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

# 3. Define the assistant's instructions.

system_message = (
    "You are usful personal mathematical assistant"
    f"Sum of input numbers"
)

# 4. Define the available tool and its input parameters.
tool = [
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Calculate the sum of two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to add."
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to add."
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]
# 5. Implement the tool and its execution logic.
def calculate_sum(a, b):
    return a + b

# 6. Prepare the initial conversation history.
def execute_tool(name, args):
    if name == "calculate_sum":
        a = args.get("a")
        b = args.get("b")
        return calculate_sum(a, b)

    return f"Unkown tool: {name}"

# 7. Send the conversation and tool definitions to the model.
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "Please calculate the sum of 22 and 68"}
]

# 8. Examine the model's response.
response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tool
)

# 9. Check how the model finished its response
finish_reason = response.choices[0].finish_reason
print(f"Finish answer: {finish_reason}")

# 9. Handle tool calls if requested
if finish_reason == "tool_calls":
    assistant_message = response.choices[0].message

    # Preserve thh assistant's message in the conversation history
    messages.append(assistant_message)

    # Process each requested tool.
    for tool_call in assistant_message.tool_calls:
        name = tool_call.function.name

        # Convert the tool call arguments from JSON to a Python dictionary
        args = json.loads(tool_call.function.arguments)

        # Execute the requested tool using execute_tool().
        tool_result = execute_tool(name, args)

        # Append the tool's result to the conversation history.
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(tool_result)
        })

    # 10. Ask the model to respond using the tool results.
    final_response = client.chat.completions.create(
        model= model,
        messages = messages,
        tools=tool
    )

    # Print the final response from the model after tool execution.
    print(final_response.choices[0].message.content)

else:
    # Print the model's response if no tool call was made.
    print(response.choices[0].message.content)