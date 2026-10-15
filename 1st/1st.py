from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
    )
    
response = client.chat.completions.create(
       model="llama3.1:8b",
       messages=[{"role":"user","content":"What is your employee code and address on this system?"}],
       )
       
print(response.choices[0].message.content)