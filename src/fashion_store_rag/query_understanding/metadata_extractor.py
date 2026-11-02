from typing import Literal

from pydantic import BaseModel, Field

from fashion_store_rag.services.llm import client

# Allowed values must match the exact taxonomy stored in Weaviate so that
# exact-match filters (Filter...equal) line up. Do not invent values outside
# these lists; use null when nothing fits.
Category = Literal[
    "Accessories",
    "Bottomwear",
    "Dresses",
    "Ethnic Wear",
    "Footwear",
    "Outerwear",
    "Topwear",
]
SubCategory = Literal[
    "Bag",
    "Belt",
    "Cap",
    "Ethnic Jacket",
    "Hoodie",
    "Jacket",
    "Jeans",
    "Kurta",
    "Leggings",
    "Midi Dress",
    "Running Shoes",
    "Scarf",
    "Shirt",
    "Shirt Dress",
    "Shorts",
    "Sneakers",
    "Sweatshirt",
    "T-Shirt",
    "Track Pants",
    "Trousers",
]
Color = Literal[
    "Beige",
    "Black",
    "Blue",
    "Brown",
    "Charcoal",
    "Green",
    "Grey",
    "Khaki",
    "Lavender",
    "Light Blue",
    "Maroon",
    "Multicolor",
    "Navy",
    "Olive",
    "Pink",
    "Red",
    "Tan",
    "White",
    "Yellow",
]
Gender = Literal["Men", "Unisex", "Women"]
Season = Literal["All Season", "Summer", "Winter"]
Usage = Literal[
    "Casual",
    "Festive",
    "Festive Casual",
    "Formal",
    "Party",
    "Sportswear",
    "Streetwear",
]


class ProductMetadata(BaseModel):
    category: Category | None = Field(
        default=None, description="Product category, such as Topwear or Bottomwear."
    )
    sub_category: SubCategory | None = Field(
        default=None, description="Product sub category, such as T-Shirt or Jeans."
    )
    color: Color | None = Field(default=None, description="Product color")
    gender: Gender | None = Field(
        default=None, description="Target gender:  Men, Women or Unisex "
    )
    fabric: str | None = Field(
        default=None,
        description="Product fabric, such as Cotton or Polyester",
    )
    season: Season | None = Field(
        default=None,
        description="Product season, such as Summer, Winter, Spring, or Autumn",
    )
    usage: Usage | None = Field(
        default=None,
        description="Product usage like, Casual, Formal, Sportswear, StreetWear, Party, Festive, Festive Casual",
    )
    sizes: list[str] | None = Field(
        default=None,
        description="Available product sizes, such as S, M, L, XL",
    )
    min_price: float | None = Field(
        default=None,
        description="Minimum product price",
    )

    max_price: float | None = Field(
        default=None,
        description="Maximum product price",
    )


def extract_metadata(query: str) -> ProductMetadata:
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": """
                You are a product metadata extraction assistant
                for a fashion store.

                Extract product attributes and price constraints
                explicitly mentioned in the customer's query.

                Rules:
                1. Extract category, subcategory, color, gender,
                   fabric, minimum price, and maximum price.
                2. Use null when an attribute is not mentioned
                   or cannot be determined confidently.
                3. Do not invent product requirements.
                4. Map category and subcategory to the store's
                   product taxonomy when clearly identifiable.
                5. For "under ₹800", set max_price to 800.
                6. For "above ₹500", set min_price to 500.
                7. For "between ₹500 and ₹1000", set both bounds.
                8. Prices are in INR.
                """,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        text_format=ProductMetadata,
    )

    return response.output_parsed
