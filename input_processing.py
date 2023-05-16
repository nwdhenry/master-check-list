import json
from typing import Any, Dict, Optional, Tuple
from reportlab.lib.units import inch


def read_input_file(input_file: str) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    try:
        with open(input_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input file '{input_file}': {e}")
        return None

    settings = data.get("settings", {})
    categories = data.get("categories", {})
    return settings, categories

def determine_columns(categories: Dict[str, Any], settings: Dict[str, Any], max_chars_per_item: int, max_chars_header: int) -> int:
    page_width, left_margin, item_font_size = (
        settings["page_width"],
        settings["left_margin"],
        settings["item_font_size"],
    )
    
    max_chars = max(max_chars_per_item, max_chars_header)
    available_width = (page_width - 2 * left_margin) * inch
    col_width = max_chars * item_font_size * 0.6

    num_columns = int(available_width // col_width)
    return max(num_columns, 1)