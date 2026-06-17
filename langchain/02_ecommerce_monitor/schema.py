from pydantic import BaseModel, Field
from typing import Optional

class ProductInfo(BaseModel):
    """Information extracted from an e-commerce product page."""
    
    product_name: str = Field(description="The full name or title of the product")
    price: Optional[float] = Field(description="The current numerical price of the product. Do not include currency symbols.")
    currency: Optional[str] = Field(description="The currency symbol or code (e.g. $, USD, ₹, INR). If not found, output None.")
    in_stock: bool = Field(description="True if the item is currently in stock or available to purchase, False if out of stock or unavailable.")
    
