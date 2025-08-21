from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("meal/<int:pk>/", views.detail, name="meal_detail"),
    path("add/", views.add_meal, name="add_meal"),
    path("history/", views.history, name="history"),
]
