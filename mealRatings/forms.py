from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Meal, Tag

class MealForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False, widget=forms.SelectMultiple(attrs={"id":"tag-select"})
    )
    class Meta:
        model = Meal
        fields = ["name","imageUrl","countryOfOrigin","description","tags"]
        widgets = {
            "name": forms.TextInput(attrs={"required": True}),
            "imageUrl": forms.TextInput(attrs={"placeholder":"e.g. 7.jpeg"}),
            "countryOfOrigin": forms.TextInput(attrs={"required": True}),
            "description": forms.Textarea(attrs={"rows":3}),
        }

class RatingForm(forms.Form):
    rating = forms.FloatField(min_value=0, max_value=5, widget=forms.NumberInput(attrs={"step":0.01}))

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name  = forms.CharField(required=False)
    email      = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2")
