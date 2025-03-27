from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
class UserMainView(LoginRequiredMixin, TemplateView):
    #Specifies what template to use when rendering the view
    template_name = 'users/main.html'
    login_url = '/login'

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
        response = super().form_valid(form)
        
        # Ensure user stays logged in after updating username or password
        update_session_auth_hash(self.request, self.object)  

        messages.success(self.request, "Profile updated successfully!")
        return response
