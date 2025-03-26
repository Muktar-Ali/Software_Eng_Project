from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from tracker.fatsecret_api import FatSecretAPI
from tracker.models import ConsumedFood 
from django.utils import timezone

User = get_user_model()

# Create your tests here.
class FatSecretAPITestCase(TestCase):
    APPLE_ID = "35718"
    TEST_USER = {
        "username": "testUser",
        "first_name": "Testing",
        "last_name": "User",
        "email": "thetestuser@gmail.com",
        "password": "BestTestUser",
        "gender": 'O',
        "age": 25,
        "height": 71,
        "weight": 138,
        "activity_level": "Light",
    }


    def setUp(self):
        """Sets up data for the test cases below"""
        self.api = FatSecretAPI()
        self.user = User.objects.create_user(**self.TEST_USER)
        self.today = timezone.now().date()


    def test_get_access_token(self):
        """Tests access token token retrieval"""
        token = self.api.get_access_token()
        self.assertIsNotNone(token, "Test failed to get access token")
    

    def test_search_food(self):
        """Tests food search function"""
        results = self.api.search_food("apple")

        self.assertIsNotNone(results, "No API result")
        self.assertIn("foods", results, "Response missing 'foods' key")

        # Checks the json structure of the test food 
        first_item = results["foods"]["food"][0]
        for field in ["food_name", "food_id", "food_description"]:
            self.assertIn(field, first_item)
        
        print(f"\nFound: {first_item['food_name']} ({first_item['food_description']})")
        # Test passed. Found: Apples (Per 100g - Calories: 52kcal | Fat: 0.17g | Carbs: 13.81g | Protein: 0.26g)


    def test_get_food(self):
        """Tests getting the food details along with servings details"""
        result = self.api.get_food(self.APPLE_ID)

        # Checks response structure
        self.assertIsNotNone(result, "API returned None")
        self.assertIn("food", result, "Response missing 'food' key")
        self.assertEqual(result["food"]["food_id"], str(self.APPLE_ID), "Incorrect food ID")

        servings = result["food"]["servings"]["serving"]
        self.assertTrue(len(servings) > 0, "No serving data found")
        self.assertIn("calories", servings[0], "Missing calories field")
        print(f"\nTest passed. Found: {result['food']['food_name']} ({servings[0]['calories']} kcal)")
        # Test passed. Found: Apples (72 kcal)
        
        
    def test_get_calories(self):
        """Tests calorie retrieval for specific food"""
        calories = self.api.get_calories(self.APPLE_ID)
        print(f"\nTest passed. Found: Calories for Apples food_id {self.APPLE_ID}: {calories} kcal")
        # Test passed. Found: Calories for Apples food_id 35718: 72 kcal


    def test_tally_calories(self):
        """Tests the calorie tally function"""  
        # Gets test food (apple)  
        apple_data = self.api.search_food("apple")
        apple_id = apple_data["foods"]["food"][0]["food_id"] # 35718
         
        # Creates a test case for 2 servings of Apples
        food_entry = ConsumedFood.objects.create(
            user = self.user,
            fatsecret_food_id = apple_id,
            servings = 2,
            date_consumed = self.today
        )
        self.assertIsNotNone(food_entry.id) # Verifies the creation of food entry

        # Gets the calories of apple and total calories
        apple_calories = self.api.get_calories(apple_id) # 72
        total_calories = self.api.tally_calories(self.user.id, self.today)

        self.assertEqual(total_calories, apple_calories * 2)
        print(f"\nTest passed. Found: Total calories: {total_calories}") # 144.0 calories"""