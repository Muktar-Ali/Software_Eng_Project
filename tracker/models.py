from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class ConsumedFood(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    fatsecret_food_id = models.CharField(
        max_length=50,
        verbose_name="FatSecret Food ID"
    )
    servings = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1)],
        verbose_name="Servings Consumed"
    )
    date_consumed = models.DateField(
        verbose_name="Date Consumed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation Time"
    )
    calories_per_serving = models.FloatField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Consumed Food"
        verbose_name_plural = "Consumed Foods"
        ordering = ['-date_consumed', '-created_at']
        unique_together = ['user', 'fatsecret_food_id', 'date_consumed']

    def __str__(self):
        return f"{self.user.username} ate {self.servings} servings on {self.date_consumed}"

    def get_calories(self, api):
        """Calculate total calories for this food entry"""
        calories = api.get_calories(self.fatsecret_food_id)
        if calories is not None:
            return calories * self.servings
        return None

class FoodHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    fatsecret_id = models.CharField(max_length=50)
    last_consumed = models.DateTimeField(auto_now=True)
    times_consumed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Food Histories"
        unique_together = ['user', 'fatsecret_id']

    def __str__(self):
        return f"{self.user.username}'s {self.food_name}"