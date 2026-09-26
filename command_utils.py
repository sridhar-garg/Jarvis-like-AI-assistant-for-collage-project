import re


def normalize_command(text: str) -> str:
    """Normalize speech for intent matching without changing the original payload text."""
    if not text:
        return ""

    text = text.lower().strip()
    text = text.replace("what's", "what is")
    text = text.replace("whats app", "whatsapp")
    text = text.replace("what s app", "whatsapp")
    text = text.replace("whatapp", "whatsapp")

    # Remove a wake word only when it is being used as a wake word.
    text = re.sub(r"^\s*(?:hey\s+|ok\s+|okay\s+)?jarvis[\s,:-]*", "", text)

    # Remove common polite wrappers that should not affect intent matching.
    text = re.sub(r"^\s*(?:please|kindly)\s+", "", text)
    text = re.sub(r"^\s*(?:can|could|would|will)\s+you\s+", "", text)
    text = re.sub(r"^\s*i\s+(?:want|need)\s+you\s+to\s+", "", text)

    # Punctuation normally produced by speech-to-text should not block matching.
    text = re.sub(r"[?,.!;]+", " ", text)

    # Articles/filler are removed ONLY from the matching copy, not from the payload.
    text = re.sub(r"\b(?:the|a|an)\b", " ", text)
    text = re.sub(r"\b(?:please|kindly|just)\b", " ", text)
    text = re.sub(r"\bfor\s+me\b", " ", text)
    text = re.sub(r"\ball\s+way\b", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def contains_any(text: str, phrases) -> bool:
    normalized = normalize_command(text)
    return any(normalize_command(phrase) in normalized for phrase in phrases)


def strip_spoken_prefix(text: str, prefixes) -> str:
    """Remove one natural-language prefix while preserving the rest as payload."""
    value = (text or "").strip()
    lowered = value.lower()
    for prefix in prefixes:
        p = prefix.lower().strip()
        if lowered.startswith(p):
            return value[len(p):].strip(" ,:-")
    return value
