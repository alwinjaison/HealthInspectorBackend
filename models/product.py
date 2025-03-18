from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class Product(BaseModel):
    barcode: str
    name: Optional[str]
    brands: Optional[str]
    categories: Optional[str]
    ingredients: Optional[str]
    image_url: Optional[str]
    nutritional_facts: Dict[str, Any]
    additives_tags: List[str]
