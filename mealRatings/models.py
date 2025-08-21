from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    TAGS = [
        ("vegetarian","vegetarian"),
        ("spicy","spicy"),
        ("healthy","healthy"),
        ("seafood","seafood"),
        ("morning","morning"),
        ("afternoon","afternoon"),
        ("evening","evening"),
    ]
    name = models.CharField(max_length=20, choices=TAGS, unique=True)

    def __str__(self): return self.name

class Meal(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    imageUrl = models.CharField(max_length=120, blank=True)  # e.g. "7.jpeg"
    countryOfOrigin = models.CharField(max_length=80)
    dateAdded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="meals")
    tags = models.ManyToManyField(Tag, blank=True, related_name="meals")

    def __str__(self): return self.name

class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="meal_ratings")
    rating = models.FloatField()  # 0–5
    dateOfRating = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dateOfRating"]
