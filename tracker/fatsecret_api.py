"""
1. Install in virtual environment to make request calls: pip install requests

2. Used the following as reference:
https://platform.fatsecret.com/docs/guides/authentication/oauth2#js

This file sends a POST request to FatSecret OAuth 2.0 and retrieves an access token.

3. **MUST INCLUDE IP ADDRESS IN 'ACCOUNT AND SETTINGS' > 'IP RESTRICTIONS'**
"""

import requests
from django.conf import settings
from django.db import models
from .models import ConsumedFood
from django.utils import timezone

class FatSecretAPI:
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
    API_URL = "https://platform.fatsecret.com/rest/server.api" # Method based integration


    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET


    # Gets the access token
    def get_access_token(self):
        response = requests.post(
            self.TOKEN_URL,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data = {
                'grant_type': 'client_credentials',
                'scope': "basic",
            },
            auth = (self.client_id, self.client_secret)
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        # Returns access token
        return response.json().get("access_token")

    
    # Searches food in the database and gives the first JSON response
    def search_food(self, query):
        # Retrieves the access token
        access_token = self.get_access_token()

        response = requests.get(
            self.API_URL,
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
            params = {
                "method": "foods.search",
                "format": "json",
                "search_expression": query
            }
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        return response.json() # Returns JSON response from FatSecret


    # Gets the food from the database
    def get_food(self, food_id):
        # Retrieves the access token
        access_token = self.get_access_token()

        response = requests.get(
            self.API_URL,
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
            params = {
                "method": "food.get",
                "food_id": str(food_id),
                "format": "json",
            }
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        return response.json() # Returns JSON response from FatSecret
    
    
    # Gets the calories from food
    def get_calories(self, food_id, serving_size=0):
        food_data = self.get_food(food_id)
        if not food_data or "food" not in food_data:
            return None

        try:
            servings = food_data["food"]["servings"]["serving"]
            if not servings:
                return None

            # Get the specified serving entry (default: first one)
            serving = servings[serving_size]
            return int(serving["calories"])

        except (KeyError, IndexError, ValueError) as e:
            print(f"Failed to parse calories: {e}")
            return None
    

    # Tallies up the calories
    def tally_calories(self, user_id, date = None):
        if date is None:
            date = timezone.now().date()
        
        # Gets all the food the user consumed
        consumed_foods = ConsumedFood.objects.filter(
            user_id = user_id,
            date_consumed = date
        )

        total_calories = 0.0

        # Calculates the total calories
        for food in consumed_foods:
            calories = self.get_calories(food.fatsecret_food_id)
            if calories is not None:
                servings = getattr(food, 'servings', 1.0)
                total_calories += float(calories) * float(food.servings)
        
        return round(total_calories, 2) # Rounds the total calories to 2 decimal places