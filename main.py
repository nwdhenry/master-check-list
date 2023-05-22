"""
Filename: main.py
Author: Nathan Henry
Date: 2023/05/22
Purpose: This module is the entry point for the PDF "master check list" generation program. 
It processes user input, calculates settings, and initiates PDF generation.
"""

import argparse
import logging
from typing import Dict, Any
from reportlab.lib.units import inch
from pdf_generation import generate_pdf
from input_processing import read_input_file
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.pdfbase.ttfonts import TTFont

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def register_fonts(settings: Dict[str, Any]) -> None:
    """
    Register the TrueType fonts specified in the settings dictionary.
    :param settings: A dictionary containing font settings.
    """
    try:
        registerFont(TTFont(settings["header_font"], f"fonts/{settings['header_font']}.ttf"))
        registerFont(TTFont(settings["item_font"], f"fonts/{settings['item_font']}.ttf"))
    except FileNotFoundError as e:
        logger.error(f"Font not found: {e}")
        raise


def determine_columns(settings: Dict[str, Any], max_width: float) -> int:
    """
    Determine the number of columns based on the available width and maximum width of the elements.
    :param settings: A dictionary containing page and layout settings.
    :param max_width: The maximum width of any element that will be placed in the columns.
    :returns: The calculated number of columns.
    """
    page_width, left_margin, right_margin = settings["page_width"], settings["left_margin"], settings["right_margin"]
    col_spacing = settings["col_spacing"]
    
    available_width = (page_width - left_margin - right_margin)
    logger.debug(f"Available width: {available_width}")
    col_width = (max_width + col_spacing) / inch
    logger.debug(f"Column width: {col_width}")
    
    num_columns = available_width // col_width
    
    # Ensure at least 1 column is generated
    return max(int(num_columns), 1)


def find_max_width(categories: Dict[str, Any], settings: Dict[str, Any], font_key: str) -> float:
    """
    Find the maximum width of elements given a certain font.
    :param categories: A dictionary containing all categories.
    :param settings: A dictionary containing page and layout settings.
    :param font_key: The font to use when calculating width.
    :returns: The maximum width found.
    """
    if font_key == "item_font":
        font = settings["item_font"]
        font_size = settings["item_font_size"]
        return max(stringWidth(item, font, font_size) for category in categories for item in categories[category])

    elif font_key == "header_font":
        font = settings["header_font"]
        font_size = settings["header_font_size"]
        return max(stringWidth(category, font, font_size) for category in categories)
    
    else:
        raise ValueError(f"Invalid font_key '{font_key}'")

def calculate_settings(settings: Dict[str, Any], max_item_width: float, max_header_width: float):
    """
    Calculate and update various settings based on the maximum widths of elements.
    :param settings: A dictionary containing page and layout settings.
    :param max_item_width: The maximum width of any item.
    :param max_header_width: The maximum width of any header.
    :returns: The updated settings dictionary.
    """
    max_width = max(max_item_width, max_header_width)
    settings["col_spacing"] = 1 * settings["item_font_size"]
    settings["num_columns"] = determine_columns(settings, max_width)
    settings["col_width"] = (max_width + settings["col_spacing"]) / inch
    settings["checkbox_size"] = 0.9 * settings["item_font_size"]
    return settings

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate checkbox list PDF from JSON file.")
    parser.add_argument("input_file", help="input JSON file")
    parser.add_argument("output_file", help="output PDF file")
    args = parser.parse_args()

    # Error handling for FileNotFoundError
    try:
        settings, categories = read_input_file(args.input_file)
    except FileNotFoundError:
        logger.error(f"Input file {args.input_file} not found.")
        raise

    if settings and categories:
        register_fonts(settings)
        max_item_width = find_max_width(categories, settings, "item_font")
        logger.debug(f"max_item_width: {max_item_width / inch} inches")
        max_header_width = find_max_width(categories, settings, "header_font")
        logger.debug(f"max_header_width: {max_header_width / inch} inches")
        settings = calculate_settings(settings, max_item_width, max_header_width)
        logger.debug(f"col_spacing: {settings['col_spacing'] / inch} inches")
        logger.debug(f"num_columns: {settings['num_columns']}")
        generate_pdf(args.output_file, settings, categories)
