import openai

openai.api_key = "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"

def chat_with_openai():
    chat_history=[]

    chat_history.append ( {"role":"system","content":"Usa un tono da teenager"})

    while True:
        user_input =input("User: ")
        chat_history.append({"role":"user", "content" : user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = chat_history
        )

        assistance_response = response.choices[0].message.get("content")
        print("Assistant: " , assistance_response)
        chat_history.append({"role": "assistant" , "content":assistance_response})
        if (user_input.lower() =="fine"):
            break


chat_with_openai()

