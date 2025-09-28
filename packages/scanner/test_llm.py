import openai

def chat_with_ai(user_input):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}  # Direct user input - potential injection
        ]
    )
    return response.choices[0].message.content

user_prompt = input("What would you like to ask? ")
result = chat_with_ai(user_prompt)
print(result)
