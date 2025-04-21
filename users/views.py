from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import localtime
# Create your views here.
class UserMainView(LoginRequiredMixin, ListView):
    #Specifies what template to use when rendering the view
    template_name = 'users/main.html'
    login_url = '/login'
    context_object_name = 'logs'
    def get_queryset(self):
        today = localtime(timezone.now()).date()
        return Log.objects.filter(user=self.request.user, log_date=today)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    success_url = '/user/profile'
    template_name = 'users/profile.html'
    form_class = ProfileUpdateForm
    login_url = '/login'
    def get_object(self, queryset=None):
        return self.request.user  # Get the currently logged-in user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the current password to the form
        kwargs['current_password'] = self.get_object().password
        return kwargs
    def form_valid(self, form):
        # Store original values before saving
        original_values = {
            'weight': self.object.weight,
            'height': self.object.height,
            'age': self.object.age,
            'gender': self.object.gender,
            'activity_level': self.object.activity_level  # Add this line
        }
        
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        
        # Check if any TDEE-relevant fields changed
        if (original_values['weight'] != self.object.weight or
            original_values['height'] != self.object.height or
            original_values['age'] != self.object.age or
            original_values['gender'] != self.object.gender or
            original_values['activity_level'] != self.object.activity_level):  # Add this line
            
            messages.info(self.request, 
                        "Your calorie targets have been updated to reflect your new profile information!")
        
        messages.success(self.request, "Profile updated successfully!")
        return response

class UserLogsView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'users/logs.html'
    login_url = '/login'
    context_object_name = 'logs'
    def get_queryset(self):
        return Log.objects.filter(user=self.request.user).order_by('-log_date')