import pyautogui
from command_utils import normalize_command


def volume_up(): pyautogui.press("up")
def volume_down(): pyautogui.press("down")
def seek_forward(): pyautogui.press("right")
def seek_backward(): pyautogui.press("left")
def seek_forward_10s(): pyautogui.press("l")
def seek_backward_10s(): pyautogui.press("j")
def seek_backward_frame(): pyautogui.press(",")
def seek_forward_frame(): pyautogui.press(".")
def seek_to_beginning(): pyautogui.press("home")
def seek_to_end(): pyautogui.press("end")
def seek_to_previous_chapter(): pyautogui.hotkey("ctrl", "left")
def seek_to_next_chapter(): pyautogui.hotkey("ctrl", "right")
def decrease_playback_speed(): pyautogui.hotkey("shift", ",")
def increase_playback_speed(): pyautogui.hotkey("shift", ".")
def move_to_next_video(): pyautogui.hotkey("shift", "n")
def move_to_previous_video(): pyautogui.hotkey("shift", "p")


def perform_media_action(text):
    text = normalize_command(text)
    actions = [
        (("volume up", "turn volume up", "increase volume", "volume badhao"), volume_up),
        (("volume down", "turn volume down", "decrease volume", "volume ghatao"), volume_down),
        (("forward 10 seconds", "seek forward 10 seconds", "10 second aage badhao"), seek_forward_10s),
        (("back 10 seconds", "backward 10 seconds", "seek backward 10 seconds", "10 second peeche karo"), seek_backward_10s),
        (("seek forward frame", "next frame", "frame aage badhao"), seek_forward_frame),
        (("seek backward frame", "previous frame", "frame peeche karo"), seek_backward_frame),
        (("seek forward", "go forward in video", "aage badhao"), seek_forward),
        (("seek backward", "go back in video", "peeche karo"), seek_backward),
        (("seek to beginning", "go to beginning", "start video", "shuruat par jao"), seek_to_beginning),
        (("seek to end", "go to end", "end video", "ant par jao"), seek_to_end),
        (("previous chapter", "seek to previous chapter"), seek_to_previous_chapter),
        (("next chapter", "seek to next chapter"), seek_to_next_chapter),
        (("decrease playback speed", "slow down video", "speed kam karo"), decrease_playback_speed),
        (("increase playback speed", "speed up video", "speed badhao"), increase_playback_speed),
        (("next video", "move to next video"), move_to_next_video),
        (("previous video", "move to previous video"), move_to_previous_video),
    ]
    for phrases, action in actions:
        if any(p in text for p in phrases):
            action()
            return True
    return False
