import pyautogui
from command_utils import normalize_command


def scroll_up():
    pyautogui.press("up", presses=5)


def scroll_down():
    pyautogui.press("down", presses=5)


def scroll_to_top():
    pyautogui.press("home")


def scroll_to_bottom():
    pyautogui.press("end")


def perform_scroll_action(text):
    text = normalize_command(text)

    if any(p in text for p in ("scroll to top", "scroll top", "go to top", "shuruat par jao")):
        scroll_to_top()
        return True
    if any(p in text for p in ("scroll to bottom", "scroll bottom", "go to bottom", "ant par jao")):
        scroll_to_bottom()
        return True
    if any(p in text for p in ("scroll up", "move up page", "upar scroll karo")):
        scroll_up()
        return True
    if any(p in text for p in ("scroll down", "move down page", "neeche scroll karo")):
        scroll_down()
        return True
    return False
