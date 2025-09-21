import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import random
import pywhatkit  # For YouTube playback

# --- Voice Settings ---
VOICE_DRIVER = "sapi5"
VOICE_RATE = 170
VOICE_VOLUME = 1.0

MUSIC_FOLDER = r"C:\Users\mayur\Music\My Playlist"  # Change this to your local music folder path

def speak(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init(VOICE_DRIVER)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", VOICE_RATE)
    engine.setProperty("volume", VOICE_VOLUME)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Play a random local song
def playLocalMusic():
    songs = [file for file in os.listdir(MUSIC_FOLDER) if file.endswith(".mp3")]
    if songs:
        song = random.choice(songs)
        speak(f"Playing {song} from local library")
        os.startfile(os.path.join(MUSIC_FOLDER, song))
    else:
        speak("No songs found in the local music library.")

# Play a song online from YouTube
def playOnlineMusic(song_name):
    speak(f"Playing {song_name} on YouTube")
    pywhatkit.playonyt(song_name)

def processCommand(command):
    command = command.lower()
    print(f"Processing command: {command}")

    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "play music" in command or "play song" in command:
        # Check if user specifies a song name
        if "online" in command or "youtube" in command:
            # extract song name after keyword
            song_name = command.replace("play", "").replace("online", "").replace("youtube", "").replace("song", "").strip()
            if song_name:
                playOnlineMusic(song_name)
            else:
                speak("Please tell me the song name to play online")
        else:
            playLocalMusic()
    else:
        speak(f"I did not understand: {command}")

if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")

            # Stop Jarvis
            if "stop" in command.lower() or "exit" in command.lower():
                speak("Shutting down. Goodbye!")
                break

            # Wake word optional
            if "jarvis" in command.lower():
                speak("Yes Sir")
            else:
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
