import requests
from config import API_BASE_URL

# ✅ Fetch product data using barcode
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

    # ✅ Calculate HealthScore
    health_score, score_details = calculate_health_score(product)

    return {
        "barcode": barcode,
        "name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "categories": product.get("categories", "Unknown"),
        "ingredients": product.get("ingredients_text", "Unknown"),
        "image_url": product.get("image_url", None),
        "nutritional_facts": product.get("nutriments", {}),
        "additives_tags": product.get("additives_tags", []),
        "health_score": health_score,
        "score_details": score_details
    }

# ✅ Search for products using a keyword
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
            # ✅ Calculate HealthScore
            health_score, score_details = calculate_health_score(product)

            results.append({
                "barcode": product.get("code", "Unknown"),
                "name": product.get("product_name", "Unknown"),
                "brands": product.get("brands", "Unknown"),
                "categories": product.get("categories", "Unknown"),
                "ingredients": product.get("ingredients_text", "Unknown"),
                "image_url": product.get("image_url", None),
                "nutritional_facts": product.get("nutriments", {}),
                "additives_tags": product.get("additives_tags", []),
                "health_score": health_score,
                "score_details": score_details
            })

    return results if results else None

# ✅ Calculate HealthScore using nutritional facts
def calculate_health_score(product):
    """Calculate HealthScore using NutriScore data if available."""
    nutriscore_data = product.get("nutriscore_data", {}).get("components", {})

    if not nutriscore_data:
        return "N/A", {"error": "NutriScore data not available"}

    # Extract positive and negative components
    negative_components = nutriscore_data.get("negative", [])
    positive_components = nutriscore_data.get("positive", [])

    # ✅ Calculate total negative and positive points
    negative_score = sum(comp.get("points", 0) for comp in negative_components)
    positive_score = sum(comp.get("points", 0) for comp in positive_components)

    # ✅ Calculate final HealthScore (negative points reduce score, positive points increase it)
    final_score = 50 - negative_score + positive_score

    # ✅ Ensure score remains within 0-100
    final_score = max(0, min(100, final_score))

    # ✅ Return HealthScore and detailed breakdown
    return final_score, {
        "negative_score": negative_score,
        "positive_score": positive_score,
        "negative_components": negative_components,
        "positive_components": positive_components,
    }
