
from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'gender', 'age', 'email', 'password', 'height', 'weight', 'activity_level']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'weight': 'Weight (pounds):',
            'height': 'Height (inches):',
            'age': 'Age (years):',
        }
        def save(self, commit=True):
            user = super().save(commit=False)
            # Hash the password before saving
            user.password = make_password(user.password)
            if commit:
                user.save()
            return user