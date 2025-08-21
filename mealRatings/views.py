from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone

from .models import Meal, MealRating, Tag
from .forms import MealForm, RatingForm, RegistrationForm

def _with_stats(qs):
    return qs.annotate(avg_rating=Avg("ratings__rating"), votes=Count("ratings"))

def _apply_filters(request, qs):
    tag_slugs = request.GET.getlist("tags")
    if tag_slugs:
        qs = qs.filter(tags__name__in=tag_slugs).distinct()
    sort = request.GET.get("sort", "date")  # date|rating|country
    if sort == "rating":
        qs = _with_stats(qs).order_by("-avg_rating", "-dateAdded")
    elif sort == "country":
        qs = qs.order_by("countryOfOrigin","-dateAdded")
    else:
        qs = qs.order_by("-dateAdded")
    return qs

def _recommended_for(user, base_qs):
    # simple collaborative filter: meals the user hasn't rated,
    # liked by users who rated the same meals highly
    my_rated = MealRating.objects.filter(user=user).values_list("meal_id", flat=True)
    similar_users = MealRating.objects.filter(meal_id__in=my_rated, rating__gte=4).exclude(user=user).values_list("user_id", flat=True)
    return (
        _with_stats(base_qs.exclude(id__in=my_rated)
        .filter(ratings__user_id__in=similar_users))
        .order_by("-avg_rating","-dateAdded")
        .distinct()
    )

def index(request):
    tags_all = list(Tag.objects.all())
    qs = Meal.objects.all()
    recommended = request.GET.get("recommended") == "1" and request.user.is_authenticated

    if recommended:
        meals = _recommended_for(request.user, Meal.objects.all())
    else:
        meals = _apply_filters(request, qs)
        meals = _with_stats(meals)

    # show only 12 on landing
    meals = meals[:12]
    selected = request.GET.getlist("tags")
    none_match = (not meals) and (selected or recommended)

    # anonymous registration form inline
    reg_form = RegistrationForm() if not request.user.is_authenticated else None
    return render(request, "mealRatings/index.html", {
        "meals": meals, "tags": tags_all, "selected": selected,
        "recommended_flag": recommended, "reg_form": reg_form, "none_match": none_match
    })

def detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    meal = _with_stats(Meal.objects.filter(pk=pk)).first()
    form = RatingForm()
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            MealRating.objects.create(
                meal=Meal.objects.get(pk=pk),
                user=request.user if request.user.is_authenticated else None,
                rating=form.cleaned_data["rating"],
                dateOfRating=timezone.now(),
            )
            messages.success(request, "Thanks for your rating!")
            return redirect("meal_detail", pk=pk)
    return render(request, "mealRatings/detail.html", {"meal": meal, "form": form})

@login_required
def add_meal(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            form.save_m2m()
            messages.success(request, "Meal added.")
            return redirect("index")
    else:
        form = MealForm()
    return render(request, "mealRatings/add.html", {"form": form})

@login_required
def history(request):
    my_meals = _with_stats(Meal.objects.filter(user=request.user)).order_by("-dateAdded")
    my_votes = (MealRating.objects.filter(user=request.user)
                .select_related("meal").order_by("-dateOfRating"))
    return render(request, "mealRatings/history.html", {"my_meals": my_meals, "my_votes": my_votes})

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})
