import speech_recognition as sr
import pyttsx3

# Configure voice settings once
VOICE_DRIVER = "sapi5"   # Windows: "sapi5", Linux: "espeak", Mac: "nsss"
VOICE_RATE = 170
VOICE_VOLUME = 1.0

def speak(text):
    print(f"Speaking: {text}")
    # Re-init engine each time to avoid queue lock
    engine = pyttsx3.init(VOICE_DRIVER)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # change index for other voices
    engine.setProperty("rate", VOICE_RATE)
    engine.setProperty("volume", VOICE_VOLUME)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processCommand(c):
    print(f"Processing: {c}")
    # Example commands
    # if "youtube" in c.lower():
    #     webbrowser.open("https://youtube.com")
    # elif "google" in c.lower():
    #     webbrowser.open("https://google.com")

if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    r = sr.Recognizer()

    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
            word = r.recognize_google(audio)
            print(f"DEBUG recognized word: {repr(word)}")

            # Flexible wake word match
            if "jarvis" in word.lower():
                speak("Ya")
                with sr.Microphone() as source:
                    print("Active Jarvis...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
