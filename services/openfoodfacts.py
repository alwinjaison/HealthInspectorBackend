import requests
from config import API_BASE_URL

def fetch_product_data(barcode: str):
    """Fetch product details using a barcode."""
    url = f"{API_BASE_URL}{barcode}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    if "product" not in data:
        return None
    
    product = data["product"]
    
    return {
        "barcode": barcode,
        "name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "categories": product.get("categories", "Unknown"),
        "ingredients": product.get("ingredients_text", "Unknown"),
        "image_url": product.get("image_url", None),
        "nutritional_facts": product.get("nutriments", {}),
        "additives_tags": product.get("additives_tags", [])
    }

def search_products(query: str):
    """Search products using a keyword with flexible matching."""
    search_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
    response = requests.get(search_url)

    if response.status_code != 200:
        return None
    
    data = response.json()
    if "products" not in data:
        return None

    products = data["products"]
    results = []
    
    query_lower = query.lower()

    for product in products:
        name = product.get("product_name", "").lower()
        brand = product.get("brands", "").lower()
        categories = product.get("categories", "").lower()
        ingredients = product.get("ingredients_text", "").lower()
        
        # ✅ Flexible matching: Add product if query appears anywhere in name, brand, category, or ingredients
        if query_lower in name or query_lower in brand or query_lower in categories or query_lower in ingredients:
            results.append({
                "barcode": product.get("code", "Unknown"),
                "name": product.get("product_name", "Unknown"),
                "brands": product.get("brands", "Unknown"),
                "categories": product.get("categories", "Unknown"),
                "ingredients": product.get("ingredients_text", "Unknown"),
                "image_url": product.get("image_url", None),
                "nutritional_facts": product.get("nutriments", {}),
                "additives_tags": product.get("additives_tags", [])
            })

    return results if results else None
