
from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password

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
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if ' ' in password:
            raise ValidationError('Password cannot contain spaces.')
        validate_password(password)
        return password
    def save(self, commit=True):
        #create a user object from the form data without saving
        user = super().save(commit=False)
        # Hash the password before saving
        user.password = make_password(user.password)
        if commit:
            #save the user object to the database
            user.save()
        return user
class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = CustomUser
        #define fields to be included in form
        fields = ['username', 'first_name', 'last_name', 'gender', 'age', 'email', 'password', 'height', 'weight', 'activity_level']
        #custom labels for the form fields
        labels = {
            'weight': 'Weight (pounds):',
            'height': 'Height (inches):',
            'age': 'Age (years):',
        }
    def __init__(self, *args, **kwargs):
        # Get the current password from kwargs
        self.current_password = kwargs.pop('current_password', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and ' ' in password:
            raise ValidationError('Password cannot contain spaces.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if password:  # Validate only if a new password is provided
            validate_password(password)
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        # Get the current password from the user object (hashed password)
        # Only hash and update the password if it's not an empty string
        # If password is an empty string, keep the current password
        if password == "":
            user.password = self.current_password
        elif password:
            # If a new password is provided, hash and set it
            user.password = make_password(password)
        if commit:
            user.save()
        return user