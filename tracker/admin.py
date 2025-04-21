from django.contrib import admin

from .models import ConsumedFood

@admin.register(ConsumedFood)
class ConsumedFoodAdmin(admin.ModelAdmin):
    list_display = ('log', 'fatsecret_food_id', 'servings', 'date_consumed', 'calories_per_serving', 'created_at')
    list_filter = ('date_consumed', 'created_at')
    search_fields = ('fatsecret_food_id', 'log__user__username')
    ordering = ('-date_consumed', '-created_at')
    autocomplete_fields = ('log',)