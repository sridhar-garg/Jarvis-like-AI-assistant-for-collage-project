import datetime
import time
import pywhatkit as kit

from TextToSpeech.Fast_DF_TTS import speak
from os import getcwd
from command_utils import normalize_command

CONTACTS = {
    "sridhar": "+919650347168",
}


def clear_file():
    with open(f"{getcwd()}\\input.txt", "w") as file:
        file.truncate(0)


def _wait_for_new_input(previous=""):
    while True:
        with open("input.txt", "r") as file:
            value = file.read().strip()
        if value and value != previous:
            return value
        time.sleep(0.1)


def _find_contact(spoken):
    normalized = normalize_command(spoken)
    for name, number in CONTACTS.items():
        if name in normalized:
            return name, number
    return None, None


def send_msg_wa():
    speak("Who do you want to send the message to, sir?")
    clear_file()

    recipient_reply = _wait_for_new_input()
    name, phone = _find_contact(recipient_reply)

    if not phone:
        speak("I could not find that person in my WhatsApp contacts list.")
        return

    speak(f"What message should I send to {name}?")
    clear_file()
    message_reply = _wait_for_new_input()

    # Keep actual message wording; only remove optional command wrappers.
    message = message_reply.strip()
    lowered = message.lower()
    for prefix in ("message is ", "send saying ", "send message ", "say "):
        if lowered.startswith(prefix):
            message = message[len(prefix):].strip()
            break

    if not message:
        speak("The message was empty, so I did not send anything.")
        return

    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=1)
    kit.sendwhatmsg(phone, message, send_time.hour, send_time.minute)
    speak("Message scheduled successfully in WhatsApp.")
