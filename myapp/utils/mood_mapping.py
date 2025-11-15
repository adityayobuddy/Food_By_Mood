# utils/mood_mapping.py
def map_mood_to_food_category(mood):
    mood = mood.lower()
    if mood == "sad":
        return ["sweet", "soft"]
    elif mood == "tired":
        return ["heavy", "protein-rich"]
    elif mood == "energetic":
        return ["light", "refreshing"]
    elif mood == "frustrated":
        return ["spicy"]
    elif mood == "stressed":
        return ["comfort", "warm"]
    elif mood == "happy":
        return ["celebration", "sweet"]
    else:
        return ["any"]
