import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import io
import random
import google.generativeai as genai

# -------------------- Configuration --------------------
MUSIC_FOLDER = r"C:\Music\JarvisSongs"  # Change to your music folder
NEWS_API_KEY = "http://feeds.bbci.co.uk/news/rss.xml"
GEMINI_API_KEY = "Your API Key"
genai.configure(api_key=GEMINI_API_KEY)

# -------------------- Initialize --------------------
recognizer = sr.Recognizer()
pygame.mixer.init()
stop_speaking = False  # Global flag to stop speech

# -------------------- Text-to-Speech --------------------
def speak(text):
    global stop_speaking
    stop_speaking = False
    if not text:
        return

    try:
        tts = gTTS(text=text, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            if stop_speaking:
                pygame.mixer.music.stop()
                break
    except Exception as e:
        print(f"TTS Error: {e}")

def stop_speech():
    global stop_speaking
    stop_speaking = True

# -------------------- Gemini AI --------------------
def ai_response(command):
    """Get short response from Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Add system instruction for short responses
        system_instruction = (
            "You are Jarvis, a helpful virtual assistant. "
            "Answer in short, concise sentences, max 2 lines."
        )
        response = model.generate_content(f"{system_instruction}\nUser: {command}")
        answer = response.text.strip()
        if not answer:
            answer = "I could not get an answer from Gemini."
        return answer
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I could not get a response from Gemini."

# -------------------- Music --------------------
def play_local_music():
    try:
        songs = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
        if songs:
            song = random.choice(songs)
            speak(f"Playing {song}")
            os.startfile(os.path.join(MUSIC_FOLDER, song))
        else:
            speak("No songs found in your music folder.")
    except Exception as e:
        speak("Error playing music.")
        print(e)

# -------------------- News --------------------
def get_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        data = r.json()
        articles = data.get("articles", [])[:5]
        if articles:
            speak("Here are the top headlines:")
            for article in articles:
                speak(article.get("title", ""))
        else:
            speak("No news available.")
    except Exception as e:
        speak("Failed to fetch news.")
        print(e)

# -------------------- Command Processor --------------------
def process_command(command):
    cmd = command.lower()
    if "stop" in cmd:
        stop_speech()
        return

    stop_speech()  # Stop any ongoing speech

    if "play music" in cmd or "play a song" in cmd:
        play_local_music()
    elif "news" in cmd or "headlines" in cmd:
        get_news()
    elif "open google" in cmd:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in cmd:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in cmd:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in cmd:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    else:
        # Use Gemini AI for general queries
        answer = ai_response(command)
        speak(answer)

# -------------------- Main Loop --------------------
if __name__ == "__main__":
    speak("Initializing Jarvis. I am online and ready.")

    # Calibrate microphone
    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=12)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if command.lower() in ["jarvis", "hey jarvis"]:
                speak("Yes sir?")
                continue
            elif command.lower().startswith("hey jarvis "):
                command = command.lower().replace("hey jarvis ", "")
                if not command:
                    speak("Yes sir?")
                    continue

            if "stop" in command.lower() or "exit" in command.lower() or "goodbye" in command.lower():
                stop_speech()
                speak("Shutting down. Goodbye!")
                break

            process_command(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.WaitTimeoutError:
            print("Listening timed out")
        except Exception as e:
            print("Error:", e)
