import re


def normalize_hypothesis_text(text: str) -> str:
    normalized = text.strip().lower()
    normalized = normalized.strip('`"\'*_')
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"[.!?]+$", "", normalized)
    return normalized
