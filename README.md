# Meal Recommender

A Django web app where users can browse, filter, and rate meals. Anonymous users can browse and rate meals, while registered users can add their own meals and view history.

## Features
- Landing page with tag filters (vegetarian, spicy, healthy, seafood, morning, afternoon, evening)  
- Sort by rating, date, or country  
- Meal detail pages with ratings  
- Authentication: register, login, logout  
- Add meals (registered users)  
- History pages (meals added and rated)  

## Tech Stack
- Python 3.12+  
- Django 5.x  
- SQLite (default, no setup required)  

## Quickstart
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or: pip install django
python manage.py migrate
python manage.py runserver 8080

Open: http://127.0.0.1:8080/
