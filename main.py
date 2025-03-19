from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from services.openfoodfacts import calculate_health_score  # Importing from openfoodfacts.py

app = FastAPI()
OPENFOODFACTS_API = "https://world.openfoodfacts.org/api/v0/product"

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_product_details(product_data):
    """Extract only required details dynamically, including HealthScore."""
    # ✅ Calculate HealthScore
    health_score, score_details = calculate_health_score(product_data)

    return {
        "barcode": product_data.get("code", "N/A"),
        "name": product_data.get("product_name", "N/A"),
        "brands": product_data.get("brands", "N/A"),
        "categories": product_data.get("categories", "N/A"),
        "ingredients": product_data.get("ingredients_text", "N/A"),
        "image_url": product_data.get("image_url", ""),
        "nutritional_facts": {
            key: value for key, value in product_data.get("nutriments", {}).items()
        },
        "additives_tags": product_data.get("additives_tags", []),
        "keywords": product_data.get("generic_name", "N/A"),
        "health_score": health_score,
        "score_details": score_details
    }

@app.get("/")
def home():
    return {"message": "HealthInspector API is running!"}

@app.get("/product/{barcode}")
async def get_product_by_barcode(barcode: str):
    """Fetch product details using barcode from OpenFoodFacts API."""
    url = f"{OPENFOODFACTS_API}/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from OpenFoodFacts.")

    data = response.json()
    if "product" not in data:
        raise HTTPException(status_code=404, detail="Product not found.")

    return extract_product_details(data["product"])

@app.get("/product/search")
async def search_product(query: str = Query(..., min_length=2)):
    """Search for a product by name, barcode, or keywords."""
    search_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
    response = requests.get(search_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error searching OpenFoodFacts.")

    data = response.json()

    # ✅ Print the entire JSON response in your terminal
    import json
    print("DEBUG: Full JSON Response:\n", json.dumps(data, indent=4))  

    return data
