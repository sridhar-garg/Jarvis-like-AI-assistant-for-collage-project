# Jarvis-like-AI-assistant-for-collage-project
JARVIS-inspired AI voice assistant for Windows powered by Gemini, with voice commands, app and web automation, WhatsApp messaging, system controls, weather, music, reminders, AI chat, and more.

JARVIS AI Assistant for Windows

A Gemini-powered JARVIS-style voice assistant for Windows with AI chat, voice commands, app and website automation, WhatsApp messaging, system controls, weather, reminders, music controls, camera vision, image generation, and more.

Features
- Gemini-powered AI chat
- Voice commands
- Open Windows applications
- Open websites
- Google search
- Browser controls
- YouTube controls
- Spotify controls
- WhatsApp messaging
- Volume control
- Brightness control
- Battery status
- Weather information
- Reminders
- Alarms
- Camera vision
- Image generation
- File creation
- Microphone checks
- Speaker checks
- Internet connectivity checking

Python Requirement
Python 3.11 is recommended.

Check your Python version:
python --version
If Python is not installed, install Python 3.11 and make sure "Add Python to PATH" is enabled during installation.

Download
Download the repository as a ZIP from GitHub and extract it anywhere on your computer.
Open PowerShell inside the extracted project folder.

Install Requirements
First upgrade pip:
python -m pip install --upgrade pip

Then install all required packages:
python -m pip install -r requirements.txt

Create a Gemini API Key
1. Go to Google AI Studio:
   https://aistudio.google.com/apikey
2. Sign in with your Google account.
3. Click Create API Key.
4. Create or select a Google Cloud project if asked.
5. Copy the generated API key.
6. Do not put the API key directly inside any Python file.

Add Gemini API Key to Windows Environment

For only the current PowerShell window:
$env:GEMINI_API_KEY="YOUR_API_KEY"
Replace YOUR_API_KEY with your actual Gemini API key.

To save the API key permanently:
setx GEMINI_API_KEY "YOUR_API_KEY"
After running the permanent command, close PowerShell or VS Code and open it again.

To check whether the API key is detected:
python -c "import os; print('Gemini API key found:', bool(os.getenv('GEMINI_API_KEY')))"
The result should be:
Gemini API key found: True

Files That Need to Be Changed

1. Time_Operations\brain.py
Change the paths for schedule.txt and Alam_data.txt to their locations on your computer.

2. Time_Operations\throw_alert.py
Change the Alam_data.txt path to the location of Alam_data.txt on your computer.

3. Alert.py
Change the logo.png path to the location of logo.png on your computer.

4. Whatsapp_automation\wa.py
Edit the CONTACTS dictionary and add your own contact names and phone numbers.

Example:

CONTACTS = {
    "dad": "+91XXXXXXXXXX",
    "mom": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX"
}

Phone numbers should include the country code.

5. Automation\Web_Data.py
Add, remove, or change website names and their URLs.
This controls the websites JARVIS can recognize and open.

6. Features\clap_with_music.py
If you want to use the clap music feature, change the MUSIC folder path to your own music folder.

7. Real_Time\google_big.py
If it contains an old chromedriver.exe path, remove the manual ChromeDriver path and use Selenium Manager instead.
Use:
driver = webdriver.Chrome(options=chrome_options)

8. Real_Time\google_small.py
If it contains an old chromedriver.exe path, remove the manual ChromeDriver path and use:
driver = webdriver.Chrome(options=chrome_options)

9. ui.py
This file is not required for the normal JARVIS version.
If you want to use the old GUI, change its old main.py path to the correct JARVIS project path.
If you do not want the GUI, simply ignore this file.

Starting JARVIS
Open PowerShell inside the main project folder and run:
python -u jarvis.py
     OR
python jarvis.py


Stopping JARVIS
Go to the PowerShell window where JARVIS is running and press:

Ctrl + C
