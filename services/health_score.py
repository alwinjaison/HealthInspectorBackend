# services/health_score.py
def calculate_health_score(product_data):
    try:
        nutriscore_data = product_data.get("nutriscore", {}).get("2023", {}).get("data", {})
        components = nutriscore_data.get("components", {})
        
        if not components:
            return None  # No health score available
        
        negative_points = sum([item.get("points", 0) for item in components.get("negative", [])])
        positive_points = sum([item.get("points", 0) for item in components.get("positive", [])])
        raw_score = negative_points - positive_points
        
        # Convert score to a 0-100 scale
        final_score = max(0, min(100, 100 - (raw_score * 2)))
        
        return final_score
    except Exception as e:
        print("Error calculating health score:", e)
        return None
