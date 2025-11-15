import requests
import json
from .recipeai import recipefromai

# from .models import Food

def get_recipe(food_name):
    
    API_URL = f"https://api.api-ninjas.com/v2/recipe?title={food_name}"
    API_KEY = "wo19mVOy5kDPpLOlw4ItAw==cABvCKlzNrvGrSSd"
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            print(data[0])
            if data[0] != None:
                return data[0]  # Return the first recipe found
            else:
                return recipefromai(food_name)
        else:
            return recipefromai(food_name)
    else:
        return recipefromai(food_name)


    