import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
import requests

from .utils.recipe import get_recipe
from .models import Food
from .utils.recommender import generate_recommendations

# Create your views here.

def home_view(request):
    return render( request,'home.html')

def about(request):
    return render( request,'about.html')

def contact(request):
    return render( request,'contact.html')

# def dynamic_url(request, name):
#     return render(request, 'dynamic.html', context = {'name': name})

def mood_questionnaire_view(request):
    
    return render(request, "questionnare.html")




# UNSPLASH_KEY = "GLOvmdIjP5OMdMfWGhqRejjfyxjL24d0eoJuUAdZ8Qg"

# def fetch_food_image(food_name):
#     url = f"https://api.unsplash.com/search/photos?query={food_name}&client_id={UNSPLASH_KEY}&per_page=1"
#     response = requests.get(url)
#     data = response.json()
#     if data["results"]:
#         return data["results"][0]["urls"]["regular"]
#     return None
import requests

def fetch_food_image(food_name,num = 1):
    API_KEY = "Your API Key"
    CX = "Your CX Key"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={food_name}&searchType=image&num={num}"

    print(url)
    response = requests.get(url)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        image_url = data["items"][0]["link"]
        if image_url.find("instagram") != -1 or image_url.find("pinterest") != -1 or image_url.find("facebook") != -1 or image_url.find("twitter") != -1 or image_url.find("food52") != -1:
            image_url = fetch_food_image(food_name,num = num + 1)
        return image_url
    return None


def bindimg(recom):
    temp = []
    for rec in recom:
        food_name = rec["name"]
        if Food.objects.filter(name__iexact=food_name).exists():
            food_obj = Food.objects.filter(name__iexact=food_name).first()
            image_url = food_obj.image_url
            if image_url == None:
                
                image_url = fetch_food_image(food_name)
            print("Image URL for", food_name, ":", image_url)
            food_obj.image_url = image_url
        
        
                
            if not food_obj.image_url and image_url:
                food_obj.image_url = image_url
                print("Updated image URL for", food_name)
        else:
            food_obj = Food.objects.create(name=food_name,image_url = fetch_food_image(food_name))
            print("Created new Food object for", food_name)
        food_obj.save()

        temp.append({
            "name": food_name,
            "image_url": image_url
        })
    print("Final temp with images:", temp)
    return temp


food_data_g = []


def recommend_foods(request, food_data):#
    # Step 1: Retrieve mood, region, weather from session or request
    mood = request.GET.get("mood") or request.session.get("mood")
    region = request.GET.get("region") or request.session.get("region")
    weather = request.GET.get("weather") or request.session.get("weather")
    hunger = request.GET.get("hunger") or request.session.get("hunger")
    

    if not mood or not region or not weather:
        return JsonResponse({"error": "Mood, region, and weather are required."}, status=400)

    # Step 2: Store them in session for later reuse (e.g. display or personalization)
    request.session["mood"] = mood
    request.session["region"] = region
    request.session["weather"] = weather
    request.session["hunger"] = hunger

    # Step 3: Get food data from DB (base data)
    # food_data = list(Food.objects.values("name", "description", "cuisine", "tags"))
    print("data loaded")

    # Step 4: Generate recommendations using LangChain
    print("22222222222222222222222222222222222222",food_data)

    recommendationsnoimg = generate_recommendations(mood, weather, region, hunger, food_data)#, food_data

    global food_data_g
    food_data_g = food_data_g + recommendationsnoimg 
    
    print("111111111111111111111111111111111111",food_data)
    
    
    
    
    recommendations = bindimg(recommendationsnoimg)
    # print(recommendations_with_images)
    # recommendations = [
    #     {"name": "Spaghetti Carbonara", "image_url": "https://images.unsplash.com/photo-1604908177523-5c3a1f4d6f4b"},
    #     {"name": "Margherita Pizza", "image_url": "https://images.unsplash.com/photo-1548365328-9aa6f1f3b3c4"},
    #     {"name": "Caesar Salad", "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141"},
    #     {"name": "Tiramisu", "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587"},
    #     {"name": "Bruschetta", "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836"}
    # ]

    # Step 5: Return JSON response
    return JsonResponse({
        "context": {
            "mood": mood,
            "region": region,
            "weather": weather,
            "hunger": hunger
        },
        # "food_data": food_data,
        "recommendations": recommendations
    })
def load_first_foods(request):
    food_data_g = []
    recommendations_response = recommend_foods(request, food_data_g)
    recommendations_data = json.loads(recommendations_response.content)
    recommendations = recommendations_data.get("recommendations", [])
    # food_data = recommendations_data.get("food_data", [])
    
     # Step 1: Retrieve mood, region, weather from session or request
    return render(request, "recommend.html",{"recommendations" : recommendations})#, "food_data": food_data


def load_more_foods(request):
    # food_data = request.GET.get("food_data")
    global food_data_g
    
    recom = recommend_foods(request, food_data_g)#    
    recom_data = json.loads(recom.content)
    recommendations = recom_data["recommendations"]#, food_data
    # recommender_data = recom_data.get("food_data", [])

    return JsonResponse({
        "recommendations": recommendations,
        # "food_data": recommender_data
    })

def custom_show_recipe(request, name):
    bindimg({"name":name})
    return show_recipe(request, name)

def show_recipe(request, name):
    
    if not name:
        return JsonResponse({"error": "Food not found."}, status=404)
    
    if Food.objects.filter(name__iexact=name).exists():
        food_obj = Food.objects.get(name__iexact=name)
    else:
        bindimg({"name":name})
    
    image_url = food_obj.recipe_img_url if food_obj.recipe_img_url else fetch_food_image(name,3)
    
    
    if not food_obj.recipe_img_url:
        food_obj.recipe_img_url = image_url
    food_obj.save()
    
    
    
    if food_obj.recipe and food_obj.ingredients:

        return render(request, "dynamic.html", context={"food_instructions": food_obj.recipe, "food_name": name, "food_ingredients": food_obj.ingredients, "food_image_url": food_obj.recipe_img_url})
            

    food_recipe = get_recipe(name)
    #JSON reponse
    # {"title": "Dish Name",
    #   "ingredients": [],
    #   "instructions": []}
    
    #saving recipe to DB
    if type(food_recipe["instructions"]) == str:
        food_recipe["instructions"] = [step.strip() for step in food_recipe["instructions"].split('.') if step.strip()]
    
    food_obj.recipe = food_recipe["instructions"]
    food_obj.ingredients = food_recipe["ingredients"]
    food_obj.save()
    
    
    return render(request, "dynamic.html", context={"food_instructions": food_recipe["instructions"], "food_name": name, "food_ingredients": food_recipe["ingredients"]})
