from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# -------------------------------
# 1️⃣ Food Catalog
# -------------------------------

class Food(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    description = models.TextField(null=True, blank=True)
    #cuisine = models.CharField(max_length=50)
    tags = models.JSONField(default=list, blank=True, null=True)     # example: ["spicy", "sweet", "warm"]
    # course = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Lunch", "Dessert"
    region = models.CharField(max_length=50, blank=True, null=True)  # region: India, china, Italy
    # popularity = models.FloatField(default=0.0)
    image_url = models.URLField(blank=True, null=True)
    # created_at = models.DateTimeField(default=timezone.now)
    ingredients = models.JSONField(default=list, null=True, blank=True)  # Optional: list of ingredients
    recipe = models.JSONField(default=list, null=True, blank=True)  # Optional: recipe instructions
    recipe_img_url = models.URLField(blank=True, null=True)  # Optional: URL to recipe image

    def __str__(self):
        return self.name


# -------------------------------
# 2️⃣ Mood / Questionnaire
# -------------------------------

# class QuestionnaireResponse(models.Model):
#     MOOD_CHOICES = [
#         ("happy", "Happy"),
#         ("sad", "Sad"),
#         ("tired", "Tired"),
#         ("stressed", "Stressed"),
#         ("energetic", "Energetic"),
#         ("frustrated", "Frustrated"),
#         ("normal", "Normal"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     session_id = models.CharField(max_length=100, blank=True, null=True)
#     mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
#     region = models.CharField(max_length=50)
#     weather = models.CharField(max_length=50)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.user or 'Guest'} - {self.mood} ({self.region})"


# # -------------------------------
# # 3️⃣ User Interactions
# # -------------------------------

# class Interaction(models.Model):
#     EVENT_CHOICES = [
#         ("view", "Viewed"),
#         ("click", "Clicked"),
#         ("like", "Liked"),
#         ("order", "Ordered"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     session_id = models.CharField(max_length=100, blank=True, null=True)
#     food = models.ForeignKey(Food, on_delete=models.CASCADE)
#     event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
#     timestamp = models.DateTimeField(default=timezone.now)
#     mood_context = models.CharField(max_length=20, blank=True, null=True)
#     weather_context = models.CharField(max_length=50, blank=True, null=True)
#     region_context = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self):
#         return f"{self.event_type} - {self.food.name}"


# # -------------------------------
# # 4️⃣ Aggregated User Preferences
# # -------------------------------

# class UserPreference(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     cuisine_scores = models.JSONField(default=dict)  # {"Indian": 3.5, "Italian": 1.2}
#     tag_scores = models.JSONField(default=dict)      # {"spicy": 2.4, "sweet": 5.1}
#     last_updated = models.DateTimeField(default=timezone.now)

#     def update_preferences(self, food):
#         """Lightweight preference update after user interacts with a food."""
#         # Update cuisine score
#         c = food.cuisine
#         t = food.tags or []

#         if c in self.cuisine_scores:
#             self.cuisine_scores[c] += 1
#         else:
#             self.cuisine_scores[c] = 1

#         # Update tag scores
#         for tag in t:
#             self.tag_scores[tag] = self.tag_scores.get(tag, 0) + 1

#         self.last_updated = timezone.now()
#         self.save()

#     def __str__(self):
#         return f"Preferences of {self.user.username}"


# # -------------------------------
# # 5️⃣ Optional: Recommendations Log
# # -------------------------------

# class RecommendationLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     session_id = models.CharField(max_length=100, blank=True, null=True)
#     context = models.JSONField(default=dict)   # {"mood": "sad", "weather": "rainy", "region": "India"}
#     recommendations = models.JSONField(default=list)  # list of food dicts
#     chosen_food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True)
#     timestamp = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Recommendations for {self.user or 'Guest'} at {self.timestamp:%Y-%m-%d %H:%M}"

