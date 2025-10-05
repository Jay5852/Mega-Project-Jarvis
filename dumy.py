import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import random
import pywhatkit
import feedparser
from gemini_module import ask_gemini

# --- Configuration ---
MUSIC_FOLDER = r"C:\Music\JarvisSongs"  # ❗ IMPORTANT: Change to your local music folder
RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"  # BBC news feed

# --- Engine Initialization ---
try:
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
except Exception as e:
    print(f"Error initializing text-to-speech engine: {e}")
    exit()

# --- Text to Speech ---
def speak(text):
    if text:
        print(f"Jarvis: {text}")
        engine.say(text)
        engine.runAndWait()

# --- NEW FUNCTION TO FIX SPEECH ISSUE ---
def clean_text(text):
    """Removes special characters that can crash the TTS engine."""
    text = text.replace("*", "")
    text = text.replace("`", "")
    text = text.replace("–", "-")
    return text

# --- Music Playback ---
def play_local_music():
    try:
        songs = [file for file in os.listdir(MUSIC_FOLDER) if file.endswith(".mp3")]
        if songs:
            song = random.choice(songs)
            speak(f"Playing {song} from your local library")
            os.startfile(os.path.join(MUSIC_FOLDER, song))
        else:
            speak("No songs were found in your music folder.")
    except FileNotFoundError:
        speak(f"I could not find the music folder at {MUSIC_FOLDER}")
    except Exception as e:
        speak("I encountered an error trying to play local music.")
        print(f"Error (play_local_music): {e}")

def play_online_music(song_name):
    try:
        speak(f"Playing {song_name} on YouTube")
        pywhatkit.playonyt(song_name)
    except Exception as e:
        speak("Sorry, I could not play music on YouTube right now.")
        print(f"Error (play_online_music): {e}")

# --- News ---
def get_news():
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            speak("Here are the latest news headlines:")
            for i, entry in enumerate(feed.entries[:5]):
                headline = clean_text(entry.title) # Also clean news headlines
                print(f"{i+1}. {headline}")
                speak(headline)
        else:
            speak("Sorry, I could not fetch the news at this moment.")
    except Exception as e:
        speak("There was a problem fetching the news feed.")
        print(f"Error (get_news): {e}")

# --- Website Opener ---
def open_website(command):
    common_sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "github": "https://www.github.com"
    }
    site_name = command.replace("open", "").strip().lower()
    if site_name in common_sites:
        url = common_sites[site_name]
        speak(f"Opening {site_name}...")
        webbrowser.open(url)
    else:
        speak(f"Searching for {site_name} on Google...")
        try:
            pywhatkit.search(site_name)
        except Exception as e:
            speak("Sorry, I could not perform the search.")
            print(f"Error (open_website search): {e}")

# --- Command Processing ---
def process_command(command):
    cmd = command.lower()
    print(f"Processing command: '{cmd}'")

    if "play music" in cmd or "play a song" in cmd:
        song_name = cmd.replace("play music", "").replace("play a song", "").strip()
        if song_name:
            play_online_music(song_name)
        else:
            play_local_music()
    elif "news" in cmd or "headlines" in cmd:
        get_news()
    elif "open" in cmd:
        open_website(cmd)
    else:
        speak("Let me think...")
        answer = ask_gemini(command)
        # --- MODIFIED LINES ---
        cleaned_answer = clean_text(answer) # Clean the answer
        speak(cleaned_answer)               # Speak the clean version

# --- Main Loop ---
if __name__ == "__main__":
    speak("Initializing Jarvis. I am online and ready.")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if "stop" in command.lower() or "exit" in command.lower() or "goodbye" in command.lower():
                speak("Shutting down. Goodbye, sir!")
                break
            
            process_command(command)

        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
        except sr.RequestError as e:
            speak("Could not connect to the speech recognition service.")
            print(f"Speech Recognition Error: {e}")
        except Exception as e:
            speak("An unexpected error occurred.")
            print(f"Main Loop Error: {e}")