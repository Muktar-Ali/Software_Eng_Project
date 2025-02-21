from django.db import models

class User(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other/Undisclosed", "Other/Undisclosed"),
    )
    
    ACTIVITY_LEVEL_CHOICES = (
        ("Sedentary", "Sedentary (office job)"),
        ("Light Exercise", "Light Exercise (1-2 days/week)"),
        ("Moderate Exercise", "Moderate Exercise (3-5 days/week)"),
        ("Heavy Exercise", "Heavy Exercise (6-7 days/week)"),
        ("Athlete", "Athlete (2x per day)"),
    )
    
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False)
    age = models.IntegerField()
    email_address = models.CharField(max_length=320)
    password = models.CharField(max_length=64)
    height = models.FloatField()
    weight = models.FloatField()
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, null=False)