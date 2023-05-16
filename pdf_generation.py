from typing import Dict, Tuple, Any

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from input_processing import read_input_file


def draw_checkbox(pdf: canvas.Canvas, x: float, y: float, checkbox_size: int) -> None:
    checkbox_x = x + 0.5 * checkbox_size
    checkbox_y = y - 0.5 * checkbox_size
    pdf.acroForm.checkbox(name='', tooltip='', x=checkbox_x, y=checkbox_y,
                          buttonStyle='check', borderWidth=0, size=checkbox_size)


def draw_header(pdf: canvas.Canvas, header: str, x: float, y: float, header_font_size: int) -> float:
    pdf.setFontSize(header_font_size)
    pdf.drawString(x, y, header)
    return y - header_font_size / 72 * inch  # Convert header_font_size to inches before subtracting


def draw_item(pdf: canvas.Canvas, item: str, x: float, y: float, checkbox_size: int, item_font_size: int, row_spacing: float) -> float:
    draw_checkbox(pdf, x, y, checkbox_size / 72 * inch)  # Convert checkbox_size to inches before drawing
    pdf.setFontSize(item_font_size)
    pdf.drawString(x + checkbox_size / 72 * inch + 5, y, item)  # Convert checkbox_size to inches before adding
    return y - item_font_size / 72 * inch - row_spacing  # Convert item_font_size to inches before subtracting


def generate_pdf(input_file: str, output_file: str, settings: Dict[str, Any], categories: Dict[str, Any]) -> None:
    # Set up the canvas and register the font
    pdf = canvas.Canvas(output_file, pagesize=(settings["page_width"] * inch, settings["page_height"] * inch))
    pdfmetrics.registerFont(TTFont(settings["header_font"], f"fonts/{settings['header_font']}.ttf"))
    pdf.setFont(settings["item_font"], 12)

    # Initialize values
    x, y = settings["left_margin"] * inch, settings["page_height"] * inch - settings["top_margin"] * inch
    col_width = (settings["page_width"] * inch - 2 * settings["left_margin"] * inch - (settings["num_columns"] - 1) * settings["col_spacing"] * inch) / settings["num_columns"]
    col_num = 0

    # Draw the headers and items
    current_y = y
    items_in_column = 0

    for header, items in categories.items():
        # Check if there's enough space for the next header in the current column
        if items_in_column + len(items) > settings["max_items_per_column"]:
            col_num += 1
            if col_num == settings["num_columns"]:
                pdf.showPage()
                col_num = 0
            current_y = settings["page_height"] * inch - settings["top_margin"] * inch
            items_in_column = 0

        current_y = draw_header(pdf, header, x + col_num * (col_width + settings["col_spacing"] * inch), current_y, settings["header_font_size"])
        current_y -= settings["header_font_size"] / 72 * inch
        items_in_column = 0

        for item in items:
            if items_in_column >= settings["max_items_per_column"]:
                col_num += 1
                if col_num == settings["num_columns"]:
                    pdf.showPage()
                    col_num = 0
                current_y = settings["page_height"] * inch - settings["top_margin"] * inch - settings["header_font_size"] / 72 * inch
                items_in_column = 0

            current_y = draw_item(pdf, item, x + col_num * (col_width + settings["col_spacing"] * inch), current_y, settings["checkbox_size"], settings["item_font_size"], settings["row_spacing"] * inch)
            items_in_column += 1

    if col_num != 0:
        pdf.showPage()

    pdf.save()