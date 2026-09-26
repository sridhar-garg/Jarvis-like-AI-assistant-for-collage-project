from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from os import getcwd


# --------------------------------------------------
# CHROME SETTINGS
# --------------------------------------------------

chrome_options = Options()

# Automatically allow microphone permission
chrome_options.add_argument("--use-fake-ui-for-media-stream")

# Run Chrome in background
chrome_options.add_argument("--headless=new")

# Extra stability options
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--log-level=3")

# Allow audio / autoplay
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")


# --------------------------------------------------
# START CHROME
# --------------------------------------------------
# IMPORTANT:
# We are NOT manually specifying chromedriver.exe anymore.
# Selenium Manager will automatically find/download
# the correct ChromeDriver for your installed Chrome version.

try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print("Could not start Chrome.")
    print("Error:", e)
    raise


# --------------------------------------------------
# SPEECH RECOGNITION WEBSITE
# --------------------------------------------------

website = "https://allorizenproject1.netlify.app/"

driver.get(website)


# --------------------------------------------------
# INPUT FILE
# --------------------------------------------------

Recog_File = f"{getcwd()}\\input.txt"


# --------------------------------------------------
# LISTEN FUNCTION
# --------------------------------------------------

def listen():

    try:

        # Wait for start button
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, "startButton")
            )
        )

        # Start speech recognition
        start_button.click()

        print("Listening...")

        output_text = ""
        is_second_click = False

        while True:

            # Find recognition output
            output_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "output")
                )
            )

            current_text = output_element.text.strip()

            # Detect recognition state
            if "Start Listening" in start_button.text and is_second_click:

                if output_text:
                    is_second_click = False

            elif "Listening..." in start_button.text:

                is_second_click = True

            # If new speech is detected
            if current_text != output_text:

                output_text = current_text

                # Save speech to input.txt
                with open(
                    Recog_File,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(output_text.lower())

                print("User:", output_text)


    except KeyboardInterrupt:

        print("\nListening stopped by user.")


    except Exception as e:

        print("An error occurred while listening:")
        print(e)


    finally:

        try:
            driver.quit()
        except:
            pass