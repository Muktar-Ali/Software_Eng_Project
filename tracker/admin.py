from django.contrib import admin

from .models import ConsumedFood, FoodHistory

@admin.register(ConsumedFood)
class ConsumedFoodAdmin(admin.ModelAdmin):
    list_display = ('user', 'fatsecret_food_id', 'servings', 'date_consumed', 'calories_per_serving', 'created_at')
    list_filter = ('user', 'date_consumed')
    search_fields = ('user__username', 'fatsecret_food_id')
    date_hierarchy = 'date_consumed'
    ordering = ('-date_consumed', '-created_at')

@admin.register(FoodHistory)
class FoodHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'fatsecret_id', 'last_consumed', 'times_consumed')
    list_filter = ('user',)
    search_fields = ('user__username', 'food_name', 'fatsecret_id')
    ordering = ('-last_consumed',)
