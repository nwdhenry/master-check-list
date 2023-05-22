import json
from typing import Any, Dict, Optional, Tuple


def read_input_file(input_file: str) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    try:
        with open(input_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.debug(f"Error: Input file '{input_file}' not found.")
        return None
    except json.JSONDecodeError as e:
        logger.debug(f"Error: Invalid JSON format in input file '{input_file}': {e}")
        return None

    settings = data.get("settings", {})
    categories = data.get("categories", {})
    return settings, categories

