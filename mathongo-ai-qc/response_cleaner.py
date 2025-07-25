import re
import json
from typing import Any


def extract_clean_json(text: str, debug: bool = False) -> Any:
    text = text.strip()

    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if not match:
        raise ValueError("No valid JSON block found in input.")

    cleaned = match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        if debug:
            print("[!] JSON decode error:", e)
            print("[!] Extracted JSON:\n", cleaned)
        raise
