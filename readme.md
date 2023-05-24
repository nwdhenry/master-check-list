
---

# Checklist PDF Generator

This program generates a "master checklist" in PDF format from a JSON input file. The generated checklist takes the form of a shopping list that is formatted to fit a specified page size. The program automatically arranges the list items in multiple columns to optimize space. This versatile tool can be used to create various checklists, from grocery lists to procedural checklists, based on the user's input file.

The program comprises three main Python modules:

- `main.py` is the entry point of the program that integrates other modules and functions.
- `pdf_generation.py` includes the function `generate_pdf`, responsible for creating the PDF file.
- `input_processing.py` provides the function `read_input_file`, which parses the JSON input file and returns the `settings` and `categories` dictionaries.

The program now includes various sorting and category fitting methods including alphabetical, numerical and custom sort. These sorting methods are defined in `settings["fit_method"]` in the JSON input file.

## Usage

To use the program, run the following command in the project's root directory:

```bash
python main.py input_file.json output_file.pdf
```

Replace `input_file.json` with the path to your JSON input file containing the list items and formatting settings, and `output_file.pdf` with the desired path for the generated PDF file.

## Input JSON File Format

The input JSON file should have the following structure:

```json
{
    "settings": {
        "page_width": float,    
        "page_height": float,   
        "left_margin": float,
        "right_margin": float,
        "top_margin": float,
        "bottom_margin": float,
        "header_font_size": int,
        "item_font_size": int,
        "header_font": "font_name",
        "item_font": "font_name",
        "row_spacing": float,
        "header_spacing": float,
        "category_spacing": float,
        "item_padding": int,
        "fit_method": "method_name"
    },
    "categories": {
        "Category 1": [
            "Item 1.1",
            "Item 1.2",
            "Item 1.3"
        ],
        "Category 2": [
            "Item 2.1",
            "Item 2.2",
            "Item 2.3"
        ]
    }
}
```

- `settings`: Contains the formatting settings for the PDF output. Page dimensions and margins are in inches. Font sizes are in points, with spacing as a multiple of the font size. `header_font` and `item_font` refer to the names of `.ttf` files in the `fonts` folder. `fit_method` determines the method used to sort the categories.
- `categories`: Contains the list items organized into categories. Each category has an array of items.

If the `settings` or `categories` fields are not present in the JSON file, an error will be logged. It's essential to ensure these fields are correctly populated.

The function `read_input_file` in `input_processing.py` loads and validates the input JSON file. Any errors in reading the file or parsing the JSON will also be logged.
Here's an example JSON input file for a grocery list:

```json
{
    "settings": {
        "page_width": 8.5,
        "page_height": 11,
        "left_margin": 0.5,
        "right_margin": 0.5,
        "top_margin": 0.5,
        "bottom_margin": 0.5,
        "header_font_size": 14,
        "item_font_size": 12,
        "header_font": "DejaVuSerif",
        "item_font": "DejaVuSerif",
        "row_spacing": 1.1,
        "header_spacing": 0.5,
        "category_spacing": 0.25,
        "item_padding": 5
    },
    "categories": {
        "Fruits & Vegetables": [
            "Apples",
            "Bananas",
            "Broccoli",
            "Carrots",
            "Cauliflower",
            "Grapes",
            "Green beans",
            "Kale",
            "Lettuce",
            "Oranges",
            "Peppers",
            "Potatoes",
            "Spinach",
            "Tomatoes",
            "Zucchini"
        ],
        "Meat & Seafood": [
            "Chicken breasts",
            "Ground beef",
            "Salmon fillets",
            "Shrimp",
            "Tilapia fillets",
            "Turkey"
        ],
        "Dairy & Eggs": [
            "Butter",
            "Cheese",
            "Eggs",
            "Milk",
            "Yogurt"
        ],
        "Grains & Pasta": [
            "Bread",
            "Brown rice",
            "Oats",
            "Pasta",
            "Quinoa"
        ],
        "Canned & Packaged Goods": [
            "Black beans",
            "Chickpeas",
            "Diced tomatoes",
            "Pasta sauce",
            "Peanut butter",
            "Tuna"
        ],
        "Snacks & Beverages": [
            "Almonds",
            "Coffee",
            "Crackers",
            "Granola bars",
            "Tea",
            "Trail mix"
        ],
        "Spices & Condiments": [
            "Balsamic vinegar",
            "Honey",
            "Ketchup",
            "Mayonnaise",
            "Olive oil",
            "Soy sauce"
        ]
    }
}
```
## Dependencies

The program requires the following Python packages to be installed:

- [ReportLab](https://www.reportlab.com/opensource/): A powerful PDF generation library.

Install the required packages using pip:

```bash
pip install reportlab
```

## Fonts

The program uses the DejaVu Serif font by default. If you want to use a different font, place the corresponding `.ttf` file in the `fonts` folder and update the `header_font` and

/or `item_font` in the JSON input file. The DejaVu fonts can be found at [DejaVu Fonts](https://dejavu-fonts.github.io/).

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for more information.

---


