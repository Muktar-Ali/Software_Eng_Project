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
import logging
from django.utils.timezone import localtime

logger = logging.getLogger(__name__)

class FatSecretAPI:
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
    API_URL = "https://platform.fatsecret.com/rest/server.api"
    TOKEN_EXPIRY = 3600  # seconds (1 hour)

    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET
        self._access_token = None
        self._token_expiry = None

    def get_access_token(self) -> str:
        """Get/refresh the access token"""
        if self._access_token and timezone.now().timestamp() < self._token_expiry:
            return self._access_token

        try:
            response = requests.post(
                self.TOKEN_URL,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={'grant_type': 'client_credentials', 'scope': "basic"},
                auth=(self.client_id, self.client_secret),
                timeout=10
            )
            
            response.raise_for_status()
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            self._token_expiry = timezone.now().timestamp() + self.TOKEN_EXPIRY
            return self._access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            return None

    def search_food(self, query: str, max_results: int = 10) -> dict:
        """Search for food items"""
        access_token = self.get_access_token()
        if not access_token:
            return None

        try:
            response = requests.get(
                self.API_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                params={
                    "method": "foods.search",
                    "format": "json",
                    "search_expression": query,
                    "max_results": max_results
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Food search failed: {e}")
            return None

    def get_food(self, food_id: str) -> dict:
        """Get detailed food information"""
        access_token = self.get_access_token()
        if not access_token:
            return None

        try:
            response = requests.get(
                self.API_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                params={
                    "method": "food.get",
                    "food_id": str(food_id),
                    "format": "json",
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get food {food_id}: {e}")
            return None

    def get_calories(self, food_id: str, serving_size: int = 0) -> int:
        """Get calories for a specific food and serving"""
        food_data = self.get_food(food_id)
        if not food_data or "food" not in food_data:
            return None

        try:
            servings = food_data["food"]["servings"]["serving"]
            if isinstance(servings, dict):  # Sometimes API returns single serving as dict
                servings = [servings]
                
            serving = servings[serving_size]
            return int(serving["calories"])
            
        except (KeyError, IndexError, ValueError, TypeError) as e:
            logger.error(f"Failed to parse calories for food {food_id}: {e}")
            return None

    def tally_calories(self, log_id: int, date=None) -> float:
        """Calculate total calories for a user on a specific date"""
        if date is None:
            date = localtime(timezone.now()).date()
        
        consumed_foods = ConsumedFood.objects.filter(
            log_id=log_id,
            date_consumed=date
        )

        total_calories = 0.0

        for food in consumed_foods:
            calories = self.get_calories(food.fatsecret_food_id)
            if calories is not None:
                total_calories += float(calories) * float(food.servings)
        
        return round(total_calories, 2)
    
    def get_nutritional_facts(self, food_id: str, serving_size: int = 0) -> dict:
        """Get nutritional facts for a specific food and serving"""
        food_data = self.get_food(food_id)
        if not food_data or "food" not in food_data:
            return None

        try:
            servings = food_data["food"]["servings"]["serving"]
            if isinstance(servings, dict):  # Handle single serving case
                servings = [servings]
                
            serving = servings[serving_size]
            return {
                'calories': serving.get("calories"),
                'protein': serving.get("protein"),
                'fat': serving.get("fat"),
                'carbs': serving.get("carbohydrate"),
                'serving_description': serving.get("serving_description")
            }
        except (KeyError, IndexError, ValueError, TypeError) as e:
            logger.error(f"Failed to parse nutrition for food {food_id}: {e}")
            return None