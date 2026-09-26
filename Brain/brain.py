import os

from google import genai

try:
    import webscout
except Exception:
    webscout = None

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Fallbacks only. Gemini is tried first.
PROVIDERS = ["Meta", "Toolbaz", "LLMChat", "SonusAI", "Netwrck", "PiAI"]


def _gemini_answer(text: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=text,
    )
    answer = (response.text or "").strip()
    return answer or None


def Main_Brain(text):
    print("Thinking...")
    last_error = None

    # Reliable primary brain using the user's Gemini API key.
    try:
        answer = _gemini_answer(text)
        if answer:
            print(f"Brain used: {GEMINI_MODEL}")
            return answer
    except Exception as e:
        last_error = e
        print("Gemini failed:", e)

    # Keep the old Webscout brains as a fallback instead of depending on them.
    if webscout is not None:
        for provider_name in PROVIDERS:
            try:
                provider_class = getattr(webscout, provider_name, None)
                if provider_class is None:
                    continue
                print(f"Trying fallback brain: {provider_name}")
                ai = provider_class()
                response = ai.chat(text)
                if response:
                    response = str(response).strip()
                    if response:
                        print(f"Fallback brain used: {provider_name}")
                        return response
            except Exception as e:
                last_error = e
                print(f"{provider_name} failed:", e)

    if not os.getenv("GEMINI_API_KEY"):
        return (
            "My Gemini API key is not configured yet. "
            "Set the GEMINI_API_KEY environment variable and restart Jarvis."
        )

    print("All online brains failed:", last_error)
    return "Sorry sir, I could not reach my AI service right now."
