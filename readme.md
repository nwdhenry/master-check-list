readme.md

# Checklist PDF Generator

This program generates a "master checklist" in PDF format using a JSON input file containing the list items and formatting settings. The program is designed to be versatile and can be used for a wide variety of use cases, from grocery lists to procedural checklists, based on the provided input file.

## Usage

To use the program, run the following command:

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
        "top_margin": float,
        "bottom_margin": float,
        "header_font_size": int,
        "item_font_size": int,
        "header_font": "font_name",
        "item_font": "font_name"
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

- `settings`: Contains the formatting settings for the PDF output, such as page dimensions, margins, font styles, and sizes.
- `categories`: Contains the list items organized into categories. Each category has an array of items.

### Example JSON Input File

Here's an example JSON input file for a grocery list:

```json
{
    "settings": {
        "page_width": 8.5,
        "page_height": 11,
        "left_margin": 0.5,
        "top_margin": 0.5,
        "bottom_margin": 0.5,
        "header_font_size": 14,
        "item_font_size": 12,
        "header_font": "DejaVuSerif",
        "item_font": "DejaVuSerif"
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

The program uses the DejaVu Serif font by default. If you want to use a different font, place the corresponding `.ttf` file in the `fonts` folder and update the `header_font` and/or `item_font` in the JSON input file.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for more information.