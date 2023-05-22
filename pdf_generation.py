"""
Filename: pdf_generation.py
Purpose: This module handles the PDF generation tasks for the "master check list" program.
It provides functions for creating checkboxes, headers, and items, and for generating a complete PDF.
Currently the page fit is a best fit algorithm, intended to pack the columns for the best fit to the page size.
"""
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Configure logging
logger = logging.getLogger(__name__)

def draw_checkbox(pdf: canvas.Canvas, x: float, y: float, checkbox_size: int) -> None:
    """Draws a checkbox at the given coordinates on the PDF."""
    checkbox_x = x + 0.25 * checkbox_size # The checkbox is drawn from the bottom left corner, so we need to adjust the x-coordinate
    checkbox_y = y - 0.125 * checkbox_size # The checkbox is drawn from the bottom left corner, so we need to adjust the y-coordinate
    pdf.acroForm.checkbox(name='', tooltip='', x=checkbox_x, y=checkbox_y,
                          buttonStyle='check', borderWidth=0, size=checkbox_size)


def draw_header(pdf: canvas.Canvas, header: str, x: float, y: float, settings: Dict[str, Any]) -> float:
    """
    Draws the header at the given coordinates on the PDF and returns the updated y-coordinate.
    :param pdf: The PDF canvas object.
    :param header: The text of the header to be drawn.
    :param x: The x-coordinate for the header.
    :param y: The y-coordinate for the header.
    :param settings: A dictionary containing page and layout settings.
    :returns: The updated y-coordinate after drawing the header.
    """
    pdf.setFont(settings["header_font"], settings["header_font_size"])
    pdf.drawString(x, y, header)
    return y - (settings["header_font_size"] + settings["row_spacing"])


def draw_item(pdf: canvas.Canvas, item: str, x: float, y: float, settings: Dict[str, Any]) -> float:
    """Draws the item at the given coordinates on the PDF and returns the updated y-coordinate."""
    draw_checkbox(pdf, x, y, settings["checkbox_size"] )
    pdf.setFont(settings["item_font"], settings["item_font_size"])
    pdf.drawString(x + settings["checkbox_size"] + settings["item_padding"], y, item)
    return y - (settings["item_font_size"] + settings["row_spacing"])


def generate_pdf(output_file: str, settings: Dict[str, Any], categories: Dict[str, Any]) -> None:
    """
    Generate a shopping list PDF given categories and settings.
    :param output_file: The path of the output PDF file.
    :param settings: A dictionary containing page and layout settings.
    :param categories: A dictionary containing all categories.
    """
    # Set up the canvas and register the font
    try:
        pdf = canvas.Canvas(output_file, pagesize=(settings["page_width"] * inch, settings["page_height"] * inch))
    
        # Initialize values
        x, y = settings["left_margin"] * inch, settings["page_height"] * inch - settings["top_margin"] * inch
        col_width = settings["col_width"] * inch
        # Sort the categories for best fit
        sorted_categories = sort_categories_for_best_fit(settings, categories)

        # Print the sorted categories for debugging
        logger.debug("Sorted Categories:")
        for col_num, column in enumerate(sorted_categories):
            logger.debug(f"Column {col_num+1}:")
            for category, items in column:
                logger.debug(f"Category: {category}")
                logger.debug(f"Items: {items}")
            logger.debug()
    
        logger.debug(f"Calculated column width: {col_width}")
        logger.debug(f"Calculated column spacing: {settings['col_spacing']}")
        logger.debug(f"Calculated row spacing: {settings['row_spacing']}")
        logger.debug(f"Calculated num columns: {settings['num_columns']}")
        # Draw the headers and items
        current_x = x
        pages = 0
        for col_num, column in enumerate(sorted_categories):
            current_y = y
        
            logger.debug(f"Coordinates for column {col_num + 1}: x: {current_x}, y: {current_y}") 

            for header, items in column:
                # Draw the header
                current_y = draw_header(pdf, header, current_x, current_y, settings)
                current_y -= settings["header_spacing"] * settings["header_font_size"]
                logger.debug(f"Drawing header at x: {current_x}, y: {current_y}")


                # Draw the items
                for item in items:
                    current_y = draw_item(pdf, item, current_x, current_y, settings)
                
                    logger.debug(f"Drawing item at x: {current_x}, y: {current_y}")

                # pad the column end.
                current_y -= settings["category_spacing"] * settings["header_font_size"]

            page_break_for_num = (col_num + 1) % settings['num_columns'] == 0
            if page_break_for_num:
                pdf.showPage()
                pages += 1
                current_x = x
                current_y = y
            else:
                current_x += col_width + settings['col_spacing'] 
            


            pdf.save()
    except IOError as e:
        logger.error(f"Unable to write to output file: {output_file}")
        raise e



def sort_categories_for_best_fit(settings: Dict[str, Any], categories: Dict[str, Any]) -> List[List[Tuple[str, List[str]]]]:
    page_height = settings["page_height"] * inch
    top_margin = settings["top_margin"] * inch
    bottom_margin = settings["bottom_margin"] * inch
    header_font_size = settings["header_font_size"]
    item_font_size = settings["item_font_size"]
    row_spacing = settings["row_spacing"]
    logger.debug(f"row spacing: {row_spacing}")
    # Calculate the heights of categories
    category_heights = {
        category: (
            (((1 + settings["header_spacing"] + settings["category_spacing"]) * header_font_size + row_spacing ) +  # Header height
            (len(items) * (item_font_size + row_spacing )))  # Items height
            
        )
        for category, items in categories.items()
    }

    # Sort the categories in decreasing order of total height
    sorted_categories = sorted(categories.items(), key=lambda item: category_heights[item[0]], reverse=True)

    # Initialize the columns
    columns: List[List[Tuple[str, List[str]]]] = [[]]
    column_heights = [page_height - top_margin - bottom_margin]
    logger.debug(f"Column Heights: {column_heights[0] / inch}")
    # Place each category in an appropriate column with enough space
    for category, items in sorted_categories:
        category_height = category_heights[category]
        logger.debug(f"Category: {category} Height: {category_height / inch} inches")
        # Find the first column with enough remaining space
        suitable_column = None
        for i, height in enumerate(column_heights):
            if height - category_height >= 0:
                suitable_column = i
                break

        # If there's a suitable column, add it there, otherwise, create a new column
        if suitable_column is not None and column_heights[suitable_column] - category_height >= 0:
            columns[suitable_column].append((category, items))
            column_heights[suitable_column] -= category_height  # Update available height
        else:
            columns.append([(category, items)])
            column_heights.append(page_height - top_margin - bottom_margin - category_height)

    # Print the column heights for debugging
    logger.debug("Column Heights:")
    for col_num, height in enumerate(column_heights):
        logger.debug(f"Column {col_num+1}: {height / inch} inches")

    return columns
