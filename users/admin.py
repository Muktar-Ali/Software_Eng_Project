from django.contrib import admin

# Register your models here.
from . import models

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "gender", "age", "email", "password", "height", "weight", "activity_level", "is_superuser", "last_login", "date_joined")
admin.site.register(models.CustomUser, CustomUserAdmin)
    

class LogAdmin(admin.ModelAdmin):
    list_display = ("dailyCalorieCount", "dailyOptimalCount", "created", "user")
admin.site.register(models.Log, LogAdmin)