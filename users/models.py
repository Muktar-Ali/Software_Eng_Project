from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
def no_whitespace_validator(value):
    if " " in value:
        raise ValidationError("This field cannot contain whitespace.")
def no_empty_string(value):
    if value == '':
        raise ValidationError('This field cannot be empty.')

# Our custom made user model which is implemented off of the AbstractUser class
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other/Undisclosed'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('Sedentary', 'Sedentary (office job)'),
        ('Light', 'Light Exercise (1-2 days/week)'),
        ('Moderate', 'Moderate Exercise (3-5 days/week)'),
        ('Heavy', 'Heavy Exercise (6-7 days/week)'),
        ('Athlete', 'Athlete (2x per day)'),
    ]
    # The username, password, email, first name and last name are already implemented by default in the AbstractUser model
    # By default, fields have the not null constraint added, so I didn't need to add it here.
    username = models.CharField(max_length=30, unique=True, validators=[no_whitespace_validator])
    first_name = models.CharField(max_length=45, validators=[no_whitespace_validator])
    last_name = models.CharField(max_length=45, validators=[no_whitespace_validator])
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=320, unique=True, validators=[no_whitespace_validator])
    height = models.FloatField(validators=[MinValueValidator(0.1)])
    weight = models.FloatField(validators=[MinValueValidator(0.1)])
    activity_level = models.CharField(max_length=50, choices=ACTIVITY_LEVEL_CHOICES)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
# The log class which contains the current daily calorie count and the optimal calorie count
class Log(models.Model):
    dailyCalorieCount = models.FloatField(default=0.0)
    dailyOptimalCount = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="log")
    @property
    def relative_date(self):
        delta = timezone.now().date() - self.created.date()
        if delta.days == 0:
            return "Today"
        elif delta.days == 1:
            return "1 day ago"
        else:
            return f"{delta.days} days ago"
    def save(self, *args, **kwargs):
        # Calculate dailyOptimalCount (TDEE) before saving the log entry
        self.dailyOptimalCount = self.calculate_tdee()
        super(Log, self).save(*args, **kwargs)

    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor Equation."""
        user = self.user
        weight = user.weight  # in kg
        height = user.height  # in cm
        age = user.age
        gender = user.gender

        # Calculate BMR using the Mifflin-St Jeor Equation
        if gender == 'M':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'F':
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age  # For 'Other' gender (or if unspecified)

        # Adjust BMR for activity level to get TDEE
        activity_multiplier = {
            'Sedentary': 1.2,
            'Light': 1.375,
            'Moderate': 1.55,
            'Heavy': 1.725,
            'Athlete': 1.9
        }

        tdee = bmr * activity_multiplier.get(user.activity_level, 1.2)  # Default to 'Sedentary' if no match

        return tdee