import pyttsx3  # Text-to-speech library
import speech_recognition as sr  # Speech recognition library

# Function for text-to-speech
engine = pyttsx3.init()

def speak(text):
    """
    Converts text to speech using pyttsx3.
    
    Args:
        text (str): The text to speak.
    """
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error during speech synthesis: {e}")


# Function for speech-to-text
def get_voice_command():
    """
    Captures and processes voice input from the user.

    Returns:
        str: The command recognized from the user's speech.
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 250  # Adjust threshold for quieter audio
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            # Capture audio input with a shorter timeout and phrase time limit
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=7)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")  # Debugging: Print captured command
            
            # Convert to lowercase for processing
            command = command.lower()
            return command
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return ""
