from django.db import models
from django.conf import settings

# Create your models here.
class ConsumedFood(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    fatsecret_food_id = models.CharField(max_length = 50)
    servings = models.FloatField(default = 1.0)
    date_consumed = models.DateField()

    def __str__(self):
        # *** EDIT LATER (SAMPLE STRING) ***
        return f"{self.user.username} ate {self.servings} servings of food id {self.fatsecret_food_id}"