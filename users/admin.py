from django.contrib import admin

# Register your models here.
from . import models

#define admin class for CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    #specify which fileds to be displayed in the list view
    list_display = ("username", "first_name", "last_name", "gender", "age", "email", "password", "height", "weight", "activity_level", "is_superuser", "last_login", "date_joined")
#register the CustomUSer model with the CustomUserAdmin configuration
admin.site.register(models.CustomUser, CustomUserAdmin)
    
#define the admin class for Log model
class LogAdmin(admin.ModelAdmin):
    #specify which fileds to be displayed in the list view
    list_display = ("dailyCalorieCount", "dailyOptimalCount", "created", "user", "log_date")
    search_fields = ["user__username"]
#register the Log model with the LogAdmin model configuration
admin.site.register(models.Log, LogAdmin)