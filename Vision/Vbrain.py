import base64
import os
import cv2
from google import genai
from google.genai import types

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def capture_image_and_save(image_path="captured_image.png"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False
    try:
        ret = False
        frame = None
        # Warm the camera up; first frame is often black/underexposed.
        for _ in range(10):
            ret, frame = cap.read()
        if ret and frame is not None:
            cv2.imwrite(image_path, frame)
            print(f"Image captured and saved as {image_path}")
            return True
        print("Error: Could not capture image.")
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def vision_brain(encoded_image, prompt="Describe what you can see in this image, including any readable text."):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "My Gemini API key is not configured, so vision is unavailable."

    try:
        image_bytes = base64.b64decode(encoded_image)
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                prompt,
            ],
        )
        return (response.text or "I could not understand the image.").strip()
    except Exception as e:
        print("Vision error:", e)
        return "I could not analyze the camera image right now."
