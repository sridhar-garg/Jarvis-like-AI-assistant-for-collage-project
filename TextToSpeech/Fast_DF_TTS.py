import pyttsx3
import pythoncom
import sys
import time
import threading


speech_lock = threading.Lock()


def print_animated_message(message):

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)

    print()


def Co_speak(message, voice="male"):

    # IMPORTANT:
    # pyttsx3/SAPI needs COM initialized
    # inside EACH thread that uses it.
    pythoncom.CoInitialize()

    engine = None

    try:

        with speech_lock:

            engine = pyttsx3.init("sapi5")

            voices = engine.getProperty("voices")

            selected_voice = None

            # Try to find a male Windows voice
            preferred_names = [
                "david",
                "mark",
                "guy"
            ]

            for preferred in preferred_names:

                for available_voice in voices:

                    if preferred in available_voice.name.lower():

                        selected_voice = available_voice.id
                        break

                if selected_voice:
                    break

            # Use selected male voice
            if selected_voice:

                engine.setProperty(
                    "voice",
                    selected_voice
                )

            elif voices:

                engine.setProperty(
                    "voice",
                    voices[0].id
                )

            # Voice speed
            engine.setProperty(
                "rate",
                180
            )

            # Maximum volume
            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(message)

            engine.runAndWait()


    except Exception as e:

        print("\nTTS Error:", e)


    finally:

        if engine is not None:

            try:
                engine.stop()
            except:
                pass

        # Release COM properly
        pythoncom.CoUninitialize()


def speak(text):

    # Voice thread
    voice_thread = threading.Thread(
        target=Co_speak,
        args=(text,)
    )

    # Terminal text animation
    text_thread = threading.Thread(
        target=print_animated_message,
        args=(text,)
    )

    voice_thread.start()
    text_thread.start()

    voice_thread.join()
    text_thread.join()


# Test
if __name__ == "__main__":

    speak(
        "Sir, I am online and ready for any duty."
    )