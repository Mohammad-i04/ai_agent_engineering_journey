from openai import OpenAI

client=OpenAI(
     api_key="ollam",
     base_url="http://localhost:11434/v1"
     )
     
prompt="Write one-sentence story about robot."

print(f"{'-'*90}")
print(f"{'temp=0.0':<45} {'temp=2.0':<45}")
print(f"{'-'*90}")

for i in range (5):
    r0=client.chat.completions.create(
    model="llama3.1:8b",
    temperature=0.0,
    messages=[{"role":"user", "content":prompt}]
    )
    
    r2=client.chat.completions.create(
    model="llama3.1:8b",
    temperature=2.0,
    messages=[{"role":"user", "content":prompt}],
    extra_body={"catch": {"no_catch": True}},
    )
    
    left=r0.choices[0].message.content.strip()[:43]
    right=r2.choices[0].message.content.strip()[:43]
    print(f"{left:<45} {right:<45}")
    
print(f"{'-'*90}")
print("\nleft: deterministic - same answer in every run")
print("\nright: random - different answer in every run")