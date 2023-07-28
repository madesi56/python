import openai

openai.api_key = "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"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user","content": "Qual'è il capoluogo della Toscana?"}
    ]
)
print (completion.choices[0].message.content)
