from Vision.Vbrain import capture_image_and_save, encode_image_to_base64, vision_brain


def mobile_vision_brain(encoded_image):
    # This uses the same Gemini vision model. The current project's capture function
    # still points at camera index 0 unless you later replace it with an IP/phone camera stream.
    return vision_brain(
        encoded_image,
        "Describe what you can see clearly. Mention important objects and any readable text.",
    )
