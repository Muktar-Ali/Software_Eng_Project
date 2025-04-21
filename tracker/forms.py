from django import forms
from django.utils import timezone
from .models import ConsumedFood  # Add this import at the top
from django.utils.timezone import localtime
class FoodSearchForm(forms.Form):
    query = forms.CharField(
        label='Search for food',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., apple, chicken breast',
            'class': 'form-control'
        })
    )

class AddConsumedFoodForm(forms.ModelForm):
    class Meta:
        model = ConsumedFood
        fields = ['servings', 'date_consumed']
    
    food_id = forms.CharField(widget=forms.HiddenInput())
    
    # These fields are already defined in the model, so we're just customizing them here
    servings = forms.FloatField(
        label='Servings',
        min_value=0.1,
        initial=1.0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'form-control'
        })
    )
    date_consumed = forms.DateField(
        label='Date consumed',
        initial=localtime(timezone.now()).date,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )