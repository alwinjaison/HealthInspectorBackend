from fastapi import APIRouter, HTTPException
from services.openfoodfacts import fetch_product_data, search_products
from schemas.product import ProductResponse

router = APIRouter()
