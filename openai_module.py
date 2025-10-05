from openai import OpenAI
from main import speak  # Import speak from main.py

# Initialize OpenAI client
client = OpenAI(api_key="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")

def ask_openai(question: str):
    """
    Send a question to OpenAI GPT and return the answer.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight, fast model
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=200
        )
        # Extract response
        answer = response.choices[0].message.content.strip()
        speak(answer)
        return answer
    except Exception as e:
        speak("Sorry, I could not get a response from OpenAI.")
        print(f"OpenAI Error: {e}")
        return None
