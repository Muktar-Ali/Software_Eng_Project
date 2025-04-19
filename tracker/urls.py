from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('search/', views.search_food, name='search_food'),
    # Handle both parameterized and non-parameterized versions
    path('add/', views.add_consumed_food, name='add_consumed_food'),  # For GET requests
    path('add/<str:food_id>/', views.add_consumed_food, name='add_consumed_food_with_param'),  # For direct access
    path('log/', views.calorie_log, name='calorie_log'),
]