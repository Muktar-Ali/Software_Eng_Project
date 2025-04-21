from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from users.models import *
class ConsumedFood(models.Model):
    log = models.ForeignKey(
        'users.Log',
        on_delete=models.CASCADE,
        related_name='consumed_foods',
        verbose_name="Log Entry",
        null=True,
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

    def get_calories(self, api):
        """Calculate total calories for this food entry"""
        calories = api.get_calories(self.fatsecret_food_id)
        if calories is not None:
            return calories * self.servings
        return None