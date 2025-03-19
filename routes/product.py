from fastapi import APIRouter, HTTPException
from services.openfoodfacts import fetch_product_data
from schemas.product import Product

router = APIRouter()

@router.get("/product/{barcode}", response_model=Product)
async def get_product(barcode: str):
    product_data = fetch_product_data(barcode)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_data
