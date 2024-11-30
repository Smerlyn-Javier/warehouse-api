from pydantic import BaseModel
from typing import List, Optional

class Supplier(BaseModel):
    name: str
    contact: str
    phone: str

class Product(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    variants: List[str]
    supplier: Supplier
    rating: Optional[float] = None
    image_url:str