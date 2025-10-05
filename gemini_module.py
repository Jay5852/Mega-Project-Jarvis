import google.generativeai as genai

# --- FIX #1: PASTE YOUR KEY HERE ---
# Get your key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "  Replace with your actual key  " # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(question, speak=None):
    try:
        # --- FIX #2: CORRECTED MODEL NAME ---
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content(question)
        answer = response.text.strip()

        if speak:
            speak(answer)  # Speak the response immediately if speak function is provided
        return answer
    except Exception as e:
        if speak:
            speak("Sorry, I could not get a response from Gemini.")
        print(f"Gemini Error: {e}")
        return None
