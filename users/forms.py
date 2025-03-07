
from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        #define fields to be included in form
        fields = ['username', 'first_name', 'last_name', 'gender', 'age', 'email', 'password', 'height', 'weight', 'activity_level']
        #specify custom input types for specific fields
        widgets = {
            'password': forms.PasswordInput(),
        }
        #custom labels for the form fields
        labels = {
            'weight': 'Weight (pounds):',
            'height': 'Height (inches):',
            'age': 'Age (years):',
        }
        def save(self, commit=True):
            #create a user object from the form data without saving
            user = super().save(commit=False)
            # Hash the password before saving
            user.password = make_password(user.password)
            if commit:
                #save the user object to the database
                user.save()
            return user