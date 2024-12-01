import os
from dotenv import load_dotenv
import pvporcupine  # Porcupine wake word library
import pyaudio      # Audio library for microphone input
import struct       # For unpacking audio stream
import os
import threading
from modules.voice_control import speak, get_voice_command
from modules.app_control import open_application, close_application

# Path to Porcupine's pre-trained wake word model
WAKE_WORD_MODEL = "models/Hola-Jarvis_en_mac_v3_0_0.ppn"  # Replace with the actual .ppn file path
load_dotenv()
ACCESS_KEY= os.getenv("ACCESS_KEY")

# Function to handle commands after the wake word
def jarvis_listen():
    """
    Activate Jarvis after the wake word is detected.
    Keeps listening for commands until the user says 'exit' or 'adios'.
    """
    speak("Hey Floppy, how can I assist you?")
    while True:
        command = get_voice_command()
        if command:
            print(f"Command received: {command}")  # Debugging: Print the received command
            execute_command(command)

            # Exit the loop if the user says "exit" or "adios"
            if "exit" in command or "adios" in command:
                break
        else:
            print("No command detected. Listening again...")
    speak("Bye Floppy!")


# Function to handle commands
def execute_command(command):
    """
    Processes and executes the user's voice command.
    
    Args:
        command (str): The user's command (e.g., "open Spotify and Chrome").
    """
    if "open" in command or "abrir" in command:
        apps = command.replace("open", "").replace("abrir", "").strip().split("and")
        for app in apps:
            app = app.strip()  # Remove extra spaces
            response = open_application(app)
            print(response)  # Print feedback to terminal
            speak(response)  # Provide feedback via voice
    elif "close" in command or "cerrar" in command:
        apps = command.replace("close", "").replace("cerrar", "").strip().split("and")
        for app in apps:
            app = app.strip()  # Remove extra spaces
            response = close_application(app)
            print(response)  # Print feedback to terminal
            speak(response)  # Provide feedback via voice
    elif "exit" in command or "ba-bye Jarvis" in command:
        speak("bye Floppy!")
        os._exit(0)
    else:
        speak("I didn't get that.")


# Function to detect the wake word
def wake_word_listener():
    """
    Starts Porcupine wake word listener.
    """
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY, 
        keyword_paths=["/Users/florenciadoval/Desktop/Jarvis/models/Hola-Jarvis_en_mac_v3_0_0.ppn"]
    )
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for the wake word...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Detect wake word
            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                jarvis_listen()  # Directly start listening for commands
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stream.close()
        audio.terminate()
        porcupine.delete()

if __name__ == "__main__":
    wake_word_listener()
