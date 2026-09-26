from Automation.open_App import open_App
from Automation.Web_Open import openweb
import pyautogui as gui
from Automation.Play_Music_YT import play_music_on_youtube
from TextToSpeech import Fast_DF_TTS
from Automation.playmusic_Sfy import play_music_on_spotify
from Automation.Battery import check_percentage
from os import getcwd
import time
from Automation.tab_automation import perform_browser_action
from Automation.Youtube_play_back import perform_media_action
import pywhatkit
from Automation.scrool_system import perform_scroll_action
import threading
from TextToSpeech.Fast_DF_TTS import speak
from command_utils import normalize_command


def play():
    gui.press("space")


def search_google(text):
    pywhatkit.search(text)


def close():
    gui.hotkey("alt", "f4")


def search(text):
    gui.press("/")
    time.sleep(0.3)
    gui.write(text)


def Open_Brain(text):
    text = normalize_command(text)
    if "website" in text:
        name = text.replace("open", "", 1).replace("website named", "").replace("website", "").strip()
        t1 = threading.Thread(target=speak, args=(f"Navigating {name} website",))
        t2 = threading.Thread(target=openweb, args=(name,))
    else:
        name = text.replace("open", "", 1).replace("app", "").replace("application", "").strip()
        t1 = threading.Thread(target=speak, args=(f"Navigating {name} application",))
        t2 = threading.Thread(target=open_App, args=(name,))
    t1.start(); t2.start(); t1.join(); t2.join()


def clear_file():
    with open(f"{getcwd()}\\input.txt", "w") as file:
        file.truncate(0)


def _wait_for_song(player):
    clear_file()
    previous = ""
    while True:
        with open("input.txt", "r") as file:
            spoken = file.read().strip()
        if spoken and spoken != previous:
            previous = spoken
            song = normalize_command(spoken)
            for prefix in ("play song", "play", "song called", "song", "called"):
                if song.startswith(prefix + " "):
                    song = song[len(prefix):].strip()
                    break
            if song:
                player(song)
                return
        time.sleep(0.1)


def Auto_main_brain(text):
    text = normalize_command(text)
    if not text:
        return False

    try:
        if text.startswith("open "):
            Open_Brain(text)
            return True

        if text in {"close", "close this", "close window", "close application", "close app"}:
            close()
            return True

        # Spotify must be checked before the generic "play music" branch.
        if "play music on spotify" in text or "play some music on spotify" in text:
            Fast_DF_TTS.speak("Which song do you want to play, sir?")
            _wait_for_song(play_music_on_spotify)
            return True

        if "play music" in text or "play music on youtube" in text:
            Fast_DF_TTS.speak("Which song do you want to play, sir?")
            _wait_for_song(play_music_on_youtube)
            return True

        if "check battery percentage" in text or "check battery level" in text or "battery percentage" in text:
            check_percentage()
            return True

        # Put the explicit Google intent before the generic search intent.
        if "search in google" in text or "google search" in text:
            query = text.replace("search in google", "").replace("google search", "").strip()
            t1 = threading.Thread(target=speak, args=(f"Searching Google for {query}",))
            t2 = threading.Thread(target=search_google, args=(query,))
            t1.start(); t2.start(); t1.join(); t2.join()
            return True

        if text.startswith("search "):
            query = text.replace("search", "", 1).strip()
            t1 = threading.Thread(target=speak, args=(f"Searching for {query}",))
            t2 = threading.Thread(target=search, args=(query,))
            t1.start(); t2.start(); t1.join(); t2.join()
            time.sleep(0.5)
            gui.press("enter")
            return True

        if text in {"play", "pause", "resume", "play video", "pause video", "resume video", "stop video"}:
            play()
            return True

        if perform_browser_action(text):
            return True
        if perform_media_action(text):
            return True
        if perform_scroll_action(text):
            return True

        return False

    except Exception as e:
        print("Automation error:", e)
        return True
