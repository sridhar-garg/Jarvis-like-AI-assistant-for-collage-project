import json
from enum import Enum
from typing import Optional

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


MODEL = "gemini-3.6-flash"


class Action(str, Enum):
    CHAT = "CHAT"
    UNKNOWN = "UNKNOWN"

    SCROLL_UP = "SCROLL_UP"
    SCROLL_DOWN = "SCROLL_DOWN"
    SCROLL_TOP = "SCROLL_TOP"
    SCROLL_BOTTOM = "SCROLL_BOTTOM"

    OPEN_NEW_TAB = "OPEN_NEW_TAB"
    CLOSE_TAB = "CLOSE_TAB"
    OPEN_BROWSER_MENU = "OPEN_BROWSER_MENU"
    ZOOM_IN = "ZOOM_IN"
    ZOOM_OUT = "ZOOM_OUT"
    REFRESH_PAGE = "REFRESH_PAGE"
    NEXT_TAB = "NEXT_TAB"
    PREVIOUS_TAB = "PREVIOUS_TAB"
    OPEN_HISTORY = "OPEN_HISTORY"
    OPEN_BOOKMARKS = "OPEN_BOOKMARKS"
    GO_BACK = "GO_BACK"
    GO_FORWARD = "GO_FORWARD"
    DEV_TOOLS = "DEV_TOOLS"
    FULL_SCREEN = "FULL_SCREEN"
    PRIVATE_WINDOW = "PRIVATE_WINDOW"

    PLAY_PAUSE = "PLAY_PAUSE"
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    SEEK_FORWARD = "SEEK_FORWARD"
    SEEK_BACKWARD = "SEEK_BACKWARD"
    SEEK_FORWARD_10S = "SEEK_FORWARD_10S"
    SEEK_BACKWARD_10S = "SEEK_BACKWARD_10S"
    SEEK_BACKWARD_FRAME = "SEEK_BACKWARD_FRAME"
    SEEK_FORWARD_FRAME = "SEEK_FORWARD_FRAME"
    VIDEO_BEGINNING = "VIDEO_BEGINNING"
    VIDEO_END = "VIDEO_END"
    PREVIOUS_CHAPTER = "PREVIOUS_CHAPTER"
    NEXT_CHAPTER = "NEXT_CHAPTER"
    DECREASE_SPEED = "DECREASE_SPEED"
    INCREASE_SPEED = "INCREASE_SPEED"
    NEXT_VIDEO = "NEXT_VIDEO"
    PREVIOUS_VIDEO = "PREVIOUS_VIDEO"

    OPEN_APP = "OPEN_APP"
    OPEN_WEBSITE = "OPEN_WEBSITE"
    CLOSE_WINDOW = "CLOSE_WINDOW"

    SEARCH_PAGE = "SEARCH_PAGE"
    SEARCH_GOOGLE = "SEARCH_GOOGLE"

    PLAY_YOUTUBE = "PLAY_YOUTUBE"
    PLAY_SPOTIFY = "PLAY_SPOTIFY"

    CHECK_BATTERY = "CHECK_BATTERY"
    WEATHER = "WEATHER"
    WHATSAPP = "WHATSAPP"

    VISION = "VISION"
    MOBILE_VISION = "MOBILE_VISION"

    GENERATE_IMAGE = "GENERATE_IMAGE"
    CREATE_FILE = "CREATE_FILE"

    CHECK_MICROPHONE = "CHECK_MICROPHONE"
    CHECK_SPEAKER = "CHECK_SPEAKER"
    CHECK_BRIGHTNESS = "CHECK_BRIGHTNESS"
    SET_BRIGHTNESS = "SET_BRIGHTNESS"
    CHECK_VOLUME = "CHECK_VOLUME"
    SET_VOLUME = "SET_VOLUME"
    CHECK_RUNNING_APPS = "CHECK_RUNNING_APPS"

    REMINDER = "REMINDER"
    SET_ALARM = "SET_ALARM"


class RouterResponse(BaseModel):
    action: Action = Field(
        description="The single best matching Jarvis action."
    )

    argument: str = Field(
        default="",
        description=(
            "Only the variable information needed by the action, such as "
            "an app name, website, location, search query, percentage, "
            "file request, alarm time, or reminder text. "
            "Use an empty string when no argument is needed."
        ),
    )


SYSTEM_PROMPT = r"""
You are the intent translator for a Windows desktop assistant named Jarvis.

Your ONLY job is to classify what the user means.
Do not answer the user's question and do not execute anything.

Rules:

1. Ignore politeness/filler such as:
   please, can you, could you, would you, for me, sir, etc.

2. Ignore the wake word Jarvis, including phrases like:
   hey Jarvis
   okay Jarvis
   Jarvis please

3. Treat different natural phrasings with the same meaning
   as the same action.

4. Preserve useful arguments closely:
   person names,
   place names,
   app names,
   website names,
   search queries,
   percentages,
   image prompts,
   file descriptions,
   times,
   reminder text.

5. Use CHAT for normal knowledge/conversation/questions that
   are not commands to control the computer or a Jarvis feature.

6. Use UNKNOWN only when the intention truly cannot be determined.

7. Never invent an argument the user did not give.

8. Return exactly one action.


Examples:

"scroll to bottom"
"scroll to the bottom"
"go all the way down"
"take me to the bottom of the page"

-> SCROLL_BOTTOM


"scroll a little down"
-> SCROLL_DOWN


"go to the top of the page"
-> SCROLL_TOP


"reload this page"
-> REFRESH_PAGE


"open another tab"
-> OPEN_NEW_TAB


"go back a page"
-> GO_BACK


"open chrome"
-> OPEN_APP
argument: "chrome"


"open youtube website"
-> OPEN_WEBSITE
argument: "youtube"


"google black holes"
"search google for black holes"

-> SEARCH_GOOGLE
argument: "black holes"


"find hello on this page"

-> SEARCH_PAGE
argument: "hello"


"play despacito on youtube"

-> PLAY_YOUTUBE
argument: "despacito"


"play shape of you on spotify"

-> PLAY_SPOTIFY
argument: "shape of you"


"what is the weather in Delhi"

-> WEATHER
argument: "Delhi"


"what is the temperature in Mumbai"

-> WEATHER
argument: "Mumbai"


"send a whatsapp message"

-> WHATSAPP


"look through the camera"

-> VISION


"what can you see using the mobile camera"

-> MOBILE_VISION


"generate an image of a red sports car"

-> GENERATE_IMAGE
argument: "a red sports car"


"set brightness to 60 percent"

-> SET_BRIGHTNESS
argument: "60"


"set volume to 35 percent"

-> SET_VOLUME
argument: "35"


"how much battery do I have"

-> CHECK_BATTERY


"remind me at 7:30 PM to study"

-> REMINDER
argument: "at 7:30 PM to study"


"set an alarm for 6:15 AM"

-> SET_ALARM
argument: "for 6:15 AM"


"why is the sky blue"

-> CHAT


"write python code for a calculator"

-> CHAT
"""


CANONICAL_COMMANDS = {

    Action.SCROLL_UP:
        "scroll up",

    Action.SCROLL_DOWN:
        "scroll down",

    Action.SCROLL_TOP:
        "scroll to top",

    Action.SCROLL_BOTTOM:
        "scroll to bottom",


    Action.OPEN_NEW_TAB:
        "open new tab",

    Action.CLOSE_TAB:
        "close tab",

    Action.OPEN_BROWSER_MENU:
        "open browser menu",

    Action.ZOOM_IN:
        "zoom in",

    Action.ZOOM_OUT:
        "zoom out",

    Action.REFRESH_PAGE:
        "refresh page",

    Action.NEXT_TAB:
        "switch to next tab",

    Action.PREVIOUS_TAB:
        "switch to previous tab",

    Action.OPEN_HISTORY:
        "open history",

    Action.OPEN_BOOKMARKS:
        "open bookmarks",

    Action.GO_BACK:
        "go back",

    Action.GO_FORWARD:
        "go forward",

    Action.DEV_TOOLS:
        "open dev tools",

    Action.FULL_SCREEN:
        "toggle full screen",

    Action.PRIVATE_WINDOW:
        "open private window",


    Action.PLAY_PAUSE:
        "play",

    Action.VOLUME_UP:
        "volume up",

    Action.VOLUME_DOWN:
        "volume down",

    Action.SEEK_FORWARD:
        "seek forward",

    Action.SEEK_BACKWARD:
        "seek backward",

    Action.SEEK_FORWARD_10S:
        "seek forward 10 seconds",

    Action.SEEK_BACKWARD_10S:
        "seek backward 10 seconds",

    Action.SEEK_BACKWARD_FRAME:
        "seek backward frame",

    Action.SEEK_FORWARD_FRAME:
        "seek forward frame",

    Action.VIDEO_BEGINNING:
        "seek to beginning",

    Action.VIDEO_END:
        "seek to end",

    Action.PREVIOUS_CHAPTER:
        "seek to previous chapter",

    Action.NEXT_CHAPTER:
        "seek to next chapter",

    Action.DECREASE_SPEED:
        "decrease playback speed",

    Action.INCREASE_SPEED:
        "increase playback speed",

    Action.NEXT_VIDEO:
        "move to next video",

    Action.PREVIOUS_VIDEO:
        "move to previous video",


    Action.CLOSE_WINDOW:
        "close",

    Action.CHECK_BATTERY:
        "check battery percentage",

    Action.WHATSAPP:
        "send message on whatsapp",

    Action.VISION:
        "what can you see",

    Action.MOBILE_VISION:
        "what can you see use mobile camera",

    Action.CHECK_MICROPHONE:
        "check microphone",

    Action.CHECK_SPEAKER:
        "check speaker",

    Action.CHECK_BRIGHTNESS:
        "check brightness percentage",

    Action.CHECK_VOLUME:
        "check volume level",

    Action.CHECK_RUNNING_APPS:
        "check running application",
}


def _clean_argument(argument: Optional[str]) -> str:

    if argument is None:
        return ""

    return str(argument).strip()


def build_jarvis_command(
    action: Action,
    argument: str
) -> Optional[str]:

    argument = _clean_argument(
        argument
    )


    if action in CANONICAL_COMMANDS:

        return CANONICAL_COMMANDS[
            action
        ]


    if action == Action.OPEN_APP:

        return (
            f"open {argument}"
            if argument
            else None
        )


    if action == Action.OPEN_WEBSITE:

        return (
            f"open website named {argument}"
            if argument
            else None
        )


    if action == Action.SEARCH_PAGE:

        return (
            f"search {argument}"
            if argument
            else None
        )


    # co_brain handles this directly.
    if action == Action.SEARCH_GOOGLE:

        return (
            f"google search {argument}"
            if argument
            else None
        )


    if action == Action.PLAY_YOUTUBE:

        return "play music on youtube"


    # Your old Automation_Brain has Spotify after its generic
    # "play music" branch.
    # "play some music" safely reaches the Spotify branch.
    if action == Action.PLAY_SPOTIFY:

        return "play some music"


    if action == Action.WEATHER:

        return (
            f"check weather in {argument}"
            if argument
            else "check weather"
        )


    if action == Action.GENERATE_IMAGE:

        return (
            f"generate image {argument}"
            if argument
            else "generate image"
        )


    if action == Action.CREATE_FILE:

        return (
            f"create file {argument}"
            if argument
            else "create file"
        )


    if action == Action.SET_BRIGHTNESS:

        return (
            f"set brightness percentage {argument}"
            if argument
            else None
        )


    if action == Action.SET_VOLUME:

        return (
            f"set volume level {argument}"
            if argument
            else None
        )


    if action == Action.REMINDER:

        return (
            f"tell me {argument}"
            if argument
            else None
        )


    if action == Action.SET_ALARM:

        return (
            f"set alarm {argument}"
            if argument
            else None
        )


    return None


def ask_gemini(
    user_text: str
) -> Optional[str]:

    """
    Used for normal questions instead of commands.
    """

    text = str(
        user_text
    ).strip()

    if not text:

        return None


    try:

        client = genai.Client()


        response = (
            client.models.generate_content(

                model=MODEL,

                contents=text,

                config=types.GenerateContentConfig(

                    system_instruction=(

                        "You are Jarvis, a concise and helpful "
                        "desktop AI assistant. "

                        "Answer the user's normal question directly. "

                        "Do not pretend to execute computer actions "
                        "unless the command router has routed an "
                        "action elsewhere."
                    ),

                    thinking_config=
                    types.ThinkingConfig(
                        thinking_level="low"
                    ),
                ),
            )
        )


        if response.text:

            return (
                response.text.strip()
            )


    except Exception as error:

        print(
            "Gemini chat error:",
            error
        )


    return None


def understand_command(
    user_text: str
) -> dict:

    text = str(
        user_text
    ).strip()


    if not text:

        return {

            "type":
                "unknown",

            "action":
                Action.UNKNOWN.value,

            "argument":
                "",

            "command":
                "",
        }


    try:

        client = genai.Client()


        response = (
            client.models.generate_content(

                model=MODEL,

                contents=text,

                config=
                types.GenerateContentConfig(

                    system_instruction=
                    SYSTEM_PROMPT,

                    response_mime_type=
                    "application/json",

                    response_schema=
                    RouterResponse,

                    thinking_config=
                    types.ThinkingConfig(
                        thinking_level=
                        "minimal"
                    ),
                ),
            )
        )


        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty router response."
            )


        data = json.loads(
            response.text
        )


        parsed = (
            RouterResponse.model_validate(
                data
            )
        )


        action = parsed.action

        argument = (
            _clean_argument(
                parsed.argument
            )
        )


        print(
            f"Gemini action: "
            f"{action.value}"
        )


        if argument:

            print(
                f"Gemini argument: "
                f"{argument}"
            )


        # -----------------------------------------
        # NORMAL QUESTION
        # -----------------------------------------

        if action == Action.CHAT:

            return {

                "type":
                    "chat",

                "action":
                    action.value,

                "argument":
                    argument,

                "command":
                    None,
            }


        # -----------------------------------------
        # UNKNOWN
        # -----------------------------------------

        if action == Action.UNKNOWN:

            return {

                "type":
                    "unknown",

                "action":
                    action.value,

                "argument":
                    argument,

                "command":
                    text.lower(),
            }


        # -----------------------------------------
        # CONVERT ACTION TO OLD JARVIS COMMAND
        # -----------------------------------------

        command = (
            build_jarvis_command(
                action,
                argument
            )
        )


        if not command:

            return {

                "type":
                    "unknown",

                "action":
                    action.value,

                "argument":
                    argument,

                "command":
                    text.lower(),
            }


        command = (
            command
            .strip()
            .lower()
        )


        print(
            f"Jarvis command: "
            f"{command}"
        )


        return {

            "type":
                "command",

            "action":
                action.value,

            "argument":
                argument,

            "command":
                command,
        }


    except Exception as error:

        print(
            "Gemini command router error:",
            error
        )


        # Gemini failure must NOT kill Jarvis.
        # Fall back to the original phrase.

        return {

            "type":
                "unknown",

            "action":
                Action.UNKNOWN.value,

            "argument":
                "",

            "command":
                text.lower(),
        }