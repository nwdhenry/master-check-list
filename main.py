import argparse
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from pdf_generation import generate_pdf
from input_processing import read_input_file, determine_columns


def find_longest_item_length(categories: Dict[str, Any]) -> int:
    max_length = 0
    for items in categories.values():
        for item in items:
            max_length = max(max_length, len(item))
    return max_length


def find_longest_header_length(categories: Dict[str, Any]) -> int:
    max_length = 0
    for header in categories.keys():
        max_length = max(max_length, len(header))
    return max_length


def calculate_max_items_per_column(settings: Dict[str, Any]) -> int:
    page_height, top_margin, bottom_margin, header_font_size, item_font_size = (
        settings["page_height"],
        settings["top_margin"],
        settings["bottom_margin"],
        settings["header_font_size"],
        settings["item_font_size"],
    )
    available_height = (page_height - top_margin - bottom_margin) * inch - header_font_size / 72 * inch
    max_items_per_column = int(available_height / (item_font_size / 72 * inch * 1.2))
    return max_items_per_column


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate checkbox list PDF from JSON file.")
    parser.add_argument("input_file", help="input JSON file")
    parser.add_argument("output_file", help="output PDF file")
    args = parser.parse_args()

    settings, categories = read_input_file(args.input_file)
    if settings and categories:
        max_chars_per_item = find_longest_item_length(categories)
        max_chars_header = find_longest_header_length(categories)
        settings["max_chars_per_item"] = max_chars_per_item
        settings["num_columns"] = determine_columns(categories, settings, max_chars_per_item, max_chars_header)
        settings["col_spacing"] = 0.2 / 72 * settings["item_font_size"] * max(max_chars_per_item, max_chars_header)
        settings["max_items_per_column"] = calculate_max_items_per_column(settings)
        settings["checkbox_size"] = settings["item_font_size"] * 0.9  # Calculate checkbox_size based on item_font_size
        settings["row_spacing"] = settings["item_font_size"] * 0.2 / 72  # Calculate row_spacing based on item_font_size and convert to inches
        generate_pdf(args.input_file, args.output_file, settings, categories)