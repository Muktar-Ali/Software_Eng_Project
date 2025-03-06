from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import SignupForm
from users.models import CustomUser

# Create your views here.
#This view inherits from Templateview
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'home/register.html'
    success_url = '/user/main'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('users.main')
        return super().get(request, *args, **kwargs)

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'

class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'

class HomeView(TemplateView):
    #Specifies what template to use when rendering the view
    template_name = 'home/welcome.html'
