import openai

openai.api_key = "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"

def test_api():
    risposta = openai.Completion.create(
        engine="text-davinci-002",
        prompt= "Chi ha creato il linguaggio Python?",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.9
    )
    print (risposta.choices[0].text.strip())



test_api()

