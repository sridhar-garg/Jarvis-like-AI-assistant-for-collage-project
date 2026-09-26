import re
import threading
import time

from Automation.Automation_Brain import (
    Auto_main_brain,
    clear_file,
    search_google,
)

from NetHyTechSTT.listen import listen

from TextToSpeech.Fast_DF_TTS import speak

from Time_Operations.brain import (
    input_manage,
    input_manage_Alam,
)

from Brain.brain import Main_Brain

from Features.create_file import create_file

from Weather_Check.check_weather import (
    get_weather_by_address
)

from Whatsapp_automation.wa import (
    send_msg_wa
)

from TextToImage.gen_image import (
    generate_image
)

from Features.mike_health import (
    mike_health
)

from Features.speaker_health import (
    speaker_health_test
)

from Features.br_persentage import (
    check_br_persentage
)

from Features.set_br import (
    set_brightness_windows
)

from Features.set_get_volume import (
    get_volume_windows,
    set_volume_windows,
)

from Features.check_running_app import (
    check_running_app
)

from AI_Command_Router import (
    understand_command,
    ask_gemini,
)


# -------------------------------------------------
# VISION
#
# Explicit imports are better than import *
# because Vbrain and MVbrain contain similarly
# named helper functions.
# -------------------------------------------------

from Vision.Vbrain import (
    capture_image_and_save,
    encode_image_to_base64,
    vision_brain,
)

from Vision.MVbrain import (
    mobile_vision_brain
)


NUMBERS = [
    "1:",
    "2:",
    "3:",
    "4:",
    "5:",
    "6:",
    "7:",
    "8:",
    "9:",
]


# =================================================
# WAKE WORD
# =================================================

def remove_wake_word(
    text: str
) -> str:

    """
    Examples:

    Jarvis scroll down
        -> scroll down

    Hey Jarvis, open Chrome
        -> open Chrome

    Okay Jarvis what is gravity
        -> what is gravity
    """

    return re.sub(

        r"^\s*"
        r"(?:(?:hey|hi|hello|ok|okay)\s+)?"
        r"jarvis"
        r"[\s,.:;!?\-]*",

        "",

        text,

        flags=re.IGNORECASE,

    ).strip()


# =================================================
# NORMAL AI CHAT
# =================================================

def handle_chat(
    user_text: str
) -> None:

    print(
        "Sending to Jarvis AI brain..."
    )


    try:

        # Gemini is the main normal-question brain.
        response = ask_gemini(
            user_text
        )


        # If Gemini has an API/network problem,
        # keep your old Brain as a backup.
        if not response:

            response = Main_Brain(
                user_text
            )


        if not response:

            response = (
                "Sorry sir, "
                "I did not get a response."
            )


        response = str(
            response
        )


        print(
            "Jarvis:",
            response
        )


        # Save conversation log
        try:

            with open(
                "log.txt",
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    "\nYou : "
                    + user_text
                )

                file.write(
                    "\nJarvis : "
                    + response
                )


        except Exception as log_error:

            print(
                "Log error:",
                log_error
            )


        speak(
            response
        )


    except Exception as error:

        print(
            "AI brain error:",
            error
        )

        speak(
            "Sorry sir, "
            "I could not process that request."
        )


# =================================================
# TIME HELPERS
# =================================================

def _normalise_time_text(
    text: str
) -> str:

    text = text.replace(
        " p.m.",
        "PM"
    )

    text = text.replace(
        " a.m.",
        "AM"
    )

    text = text.replace(
        " pm",
        "PM"
    )

    text = text.replace(
        " am",
        "AM"
    )

    return text


# =================================================
# REMINDER
# =================================================

def handle_tell_me(
    output_text: str
) -> None:

    output_text = (
        _normalise_time_text(
            output_text
        )
    )


    if (
        "11:" in output_text
        or
        "12:" in output_text
    ):

        input_manage(
            output_text
        )

        clear_file()

        return


    for number in NUMBERS:

        if number in output_text:

            output_text = (
                output_text.replace(
                    number,
                    f"0{number}"
                )
            )

            input_manage(
                output_text
            )

            clear_file()

            return


    # Let old time parser try anyway
    input_manage(
        output_text
    )

    clear_file()


# =================================================
# ALARM
# =================================================

def handle_alarm(
    output_text: str
) -> None:

    output_text = (
        _normalise_time_text(
            output_text
        )
    )


    if (
        "11:" in output_text
        or
        "12:" in output_text
    ):

        input_manage_Alam(
            output_text
        )

        clear_file()

        return


    for number in NUMBERS:

        if number in output_text:

            output_text = (
                output_text.replace(
                    number,
                    f"0{number}"
                )
            )

            input_manage_Alam(
                output_text
            )

            clear_file()

            return


    input_manage_Alam(
        output_text
    )

    clear_file()


# =================================================
# NUMBER EXTRACTION
# =================================================

def _extract_number(
    text: str
) -> int:

    match = re.search(
        r"-?\d+",
        text
    )


    if not match:

        raise ValueError(
            "No numeric value was found "
            "in the command."
        )


    return int(
        match.group()
    )


# =================================================
# MAIN INPUT LOOP
# =================================================

def check_inputs() -> None:

    previous_raw_input = ""


    while True:

        try:

            # -------------------------------------
            # READ SPEECH RECOGNITION OUTPUT
            # -------------------------------------

            with open(
                "input.txt",
                "r",
                encoding="utf-8"
            ) as file:

                raw_input = (
                    file
                    .read()
                    .strip()
                )


            # Nothing spoken
            if not raw_input:

                previous_raw_input = ""

                time.sleep(
                    0.05
                )

                continue


            # Prevent same speech result
            # from executing repeatedly
            if (
                raw_input
                ==
                previous_raw_input
            ):

                time.sleep(
                    0.05
                )

                continue


            previous_raw_input = (
                raw_input
            )


            print()

            print(
                "User:",
                raw_input
            )


            # =====================================
            # REMOVE WAKE WORD
            # =====================================

            command_input = (
                remove_wake_word(
                    raw_input
                )
            )


            print(
                "After wake word removal:",
                command_input
            )


            # User only said:
            #
            # Jarvis
            # Hey Jarvis
            #
            if not command_input:

                speak(
                    "Yes sir?"
                )

                clear_file()

                previous_raw_input = ""

                continue


            # =====================================
            # SEND TO GEMINI COMMAND ROUTER
            # =====================================

            print(
                "Understanding command..."
            )


            result = (
                understand_command(
                    command_input
                )
            )


            print(
                "Router result:",
                result
            )


            # =====================================
            # NORMAL QUESTION
            # =====================================

            if (
                result["type"]
                ==
                "chat"
            ):

                handle_chat(
                    command_input
                )

                clear_file()

                previous_raw_input = ""

                continue


            # =====================================
            # COMMAND
            # =====================================

            if (
                result["type"]
                ==
                "command"
            ):

                output_text = (
                    result["command"]
                )


            # =====================================
            # GEMINI FAILED / UNKNOWN
            # =====================================

            else:

                # Let old Jarvis try original words
                output_text = (
                    command_input
                    .lower()
                    .strip()
                )


            print(
                "Executing:",
                output_text
            )


            # =====================================
            # REMINDER
            # =====================================

            if output_text.startswith(
                "tell me"
            ):

                handle_tell_me(
                    output_text
                )


            # =====================================
            # ALARM
            # =====================================

            elif output_text.startswith(
                "set alarm"
            ):

                handle_alarm(
                    output_text
                )


            # =====================================
            # CREATE FILE
            # =====================================

            elif (
                output_text.startswith(
                    "create"
                )
                and
                "file" in output_text
            ):

                create_file(
                    output_text
                )

                clear_file()


            # =====================================
            # LAPTOP CAMERA VISION
            # =====================================

            elif (
                (
                    "what is this"
                    in output_text
                    or
                    "what can you see"
                    in output_text
                )
                and
                "mobile"
                not in output_text
            ):

                image_path = (
                    "captured_image.png"
                )


                if capture_image_and_save(
                    image_path
                ):

                    encoded_image = (
                        encode_image_to_base64(
                            image_path
                        )
                    )


                    answer = vision_brain(
                        encoded_image
                    )


                    if answer:

                        speak(
                            str(answer)
                        )


                clear_file()


            # =====================================
            # MOBILE VISION
            # =====================================

            elif (
                "what is in front of mobile camera"
                in output_text
                or
                "what can you see use mobile camera"
                in output_text
            ):

                image_path = (
                    "captured_image.png"
                )


                if capture_image_and_save(
                    image_path
                ):

                    encoded_image = (
                        encode_image_to_base64(
                            image_path
                        )
                    )


                    answer = (
                        mobile_vision_brain(
                            encoded_image
                        )
                    )


                    if answer:

                        speak(
                            str(answer)
                        )


                clear_file()


            # =====================================
            # WEATHER
            # =====================================

            elif (
                "check weather"
                in output_text
            ):

                location = (

                    output_text

                    .replace(
                        "check weather in",
                        ""
                    )

                    .replace(
                        "check weather",
                        ""
                    )

                    .strip()
                )


                if not location:

                    speak(
                        "Which place should I "
                        "check the weather for, sir?"
                    )


                else:

                    print(
                        "Weather location:",
                        location
                    )


                    answer = (
                        get_weather_by_address(
                            location
                        )
                    )


                    if answer:

                        speak(
                            str(answer)
                        )


                clear_file()


            # =====================================
            # WHATSAPP
            # =====================================

            elif (
                "send message on whatsapp"
                in output_text
            ):

                # Existing function asks who,
                # then asks for message.
                send_msg_wa()

                clear_file()


            # =====================================
            # IMAGE GENERATION
            # =====================================

            elif (
                "generate image"
                in output_text
            ):

                prompt = (

                    output_text

                    .replace(
                        "generate image",
                        ""
                    )

                    .strip()
                )


                if prompt:

                    generate_image(
                        prompt
                    )

                    speak(
                        "Image generated successfully"
                    )


                else:

                    speak(
                        "What image would you like "
                        "me to generate, sir?"
                    )


                clear_file()


            # =====================================
            # MICROPHONE
            # =====================================

            elif (
                "check mike"
                in output_text
                or
                "check mike health"
                in output_text
                or
                "check microphone"
                in output_text
            ):

                mike_health()

                clear_file()


            # =====================================
            # SPEAKER
            # =====================================

            elif (
                "check speaker health"
                in output_text
                or
                "check speaker"
                in output_text
            ):

                speaker_health_test()

                clear_file()


            # =====================================
            # BRIGHTNESS
            # =====================================

            elif (
                "check brightness percentage"
                in output_text
            ):

                check_br_persentage()

                clear_file()


            elif (
                "set brightness percentage"
                in output_text
            ):

                value = (
                    _extract_number(
                        output_text
                    )
                )


                value = max(
                    0,
                    min(
                        100,
                        value
                    )
                )


                set_brightness_windows(
                    value
                )

                clear_file()


            # =====================================
            # VOLUME
            # =====================================

            elif (
                "check volume level"
                in output_text
            ):

                get_volume_windows()

                clear_file()


            elif (
                "set volume level"
                in output_text
            ):

                value = (
                    _extract_number(
                        output_text
                    )
                )


                value = max(
                    0,
                    min(
                        100,
                        value
                    )
                )


                set_volume_windows(
                    value
                )

                clear_file()


            # =====================================
            # RUNNING APPS
            # =====================================

            elif (
                "check running application"
                in output_text
            ):

                check_running_app()

                clear_file()


            # =====================================
            # GOOGLE SEARCH
            # =====================================
            #
            # Your old Automation_Brain checks
            # startswith("search") before checking
            # "search in google".
            #
            # So Gemini creates:
            #
            # google search black holes
            #
            # and we handle it here.
            # =====================================

            elif output_text.startswith(
                "google search "
            ):

                query = (

                    output_text

                    .removeprefix(
                        "google search "
                    )

                    .strip()
                )


                if query:

                    speak(
                        f"Searching Google for {query}"
                    )


                    search_google(
                        query
                    )


                clear_file()


            # =====================================
            # EVERYTHING ELSE
            # =====================================
            #
            # This includes:
            #
            # scroll
            # open apps
            # open websites
            # browser controls
            # tabs
            # media
            # YouTube
            # Spotify
            # battery
            # page search
            #
            # =====================================

            else:

                Auto_main_brain(
                    output_text
                )

                clear_file()


            # Lets you use exact same command again
            previous_raw_input = ""


        except Exception as error:

            print(
                "co_brain error:",
                error
            )


            try:

                clear_file()

            except Exception:

                pass


            previous_raw_input = ""

            time.sleep(
                0.1
            )


# =================================================
# START JARVIS
# =================================================

def Jarvis() -> None:

    clear_file()


    listener_thread = (
        threading.Thread(
            target=listen
        )
    )


    command_thread = (
        threading.Thread(
            target=check_inputs
        )
    )


    listener_thread.start()

    command_thread.start()


    listener_thread.join()

    command_thread.join()