import pyautogui
from command_utils import normalize_command


def open_new_tab(): pyautogui.hotkey("ctrl", "t")
def close_tab(): pyautogui.hotkey("ctrl", "w")
def open_browser_menu(): pyautogui.hotkey("alt", "f")
def zoom_in(): pyautogui.hotkey("ctrl", "+")
def zoom_out(): pyautogui.hotkey("ctrl", "-")
def refresh_page(): pyautogui.hotkey("ctrl", "r")
def switch_to_next_tab(): pyautogui.hotkey("ctrl", "tab")
def switch_to_previous_tab(): pyautogui.hotkey("ctrl", "shift", "tab")
def open_history(): pyautogui.hotkey("ctrl", "h")
def open_bookmarks(): pyautogui.hotkey("ctrl", "b")
def go_back(): pyautogui.hotkey("alt", "left")
def go_forward(): pyautogui.hotkey("alt", "right")
def open_dev_tools(): pyautogui.hotkey("ctrl", "shift", "i")
def toggle_full_screen(): pyautogui.press("f11")
def open_private_window(): pyautogui.hotkey("ctrl", "shift", "n")


def perform_browser_action(text):
    text = normalize_command(text)
    actions = [
        (("open new tab", "new tab kholo", "make new tab"), open_new_tab),
        (("close tab", "tab band karo"), close_tab),
        (("open browser menu", "browser menu kholo"), open_browser_menu),
        (("zoom in", "zoom in karo"), zoom_in),
        (("zoom out", "zoom out karo"), zoom_out),
        (("refresh page", "reload page", "page refresh karo"), refresh_page),
        (("switch to next tab", "go to next tab", "next tab par jao"), switch_to_next_tab),
        (("switch to previous tab", "go to previous tab", "previous tab par jao"), switch_to_previous_tab),
        (("open history", "history kholo"), open_history),
        (("open bookmarks", "bookmarks kholo"), open_bookmarks),
        (("go back", "back page", "peeche jao"), go_back),
        (("go forward", "forward page", "aage jao"), go_forward),
        (("open dev tools", "open developer tools", "dev tools kholo"), open_dev_tools),
        (("toggle full screen", "full screen", "fullscreen"), toggle_full_screen),
        (("open private window", "open incognito", "private window kholo"), open_private_window),
    ]
    for phrases, action in actions:
        if any(p in text for p in phrases):
            action()
            return True
    return False
