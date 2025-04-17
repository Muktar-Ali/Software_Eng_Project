from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import SignupForm
from users.models import *
from django.utils import timezone
from datetime import timedelta
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
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def handle_user_login(self, user):
        today = timezone.now().date()
        
        # Check if a log exists for today
        if not Log.objects.filter(user=user, created__date=today).exists():
            Log.objects.create(user=user)
        
        # Delete logs older than 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        Log.objects.filter(user=user, created__lt=seven_days_ago).delete()

    def form_valid(self, form):
        # runs the previous method after a successful login
        response = super().form_valid(form)
        self.handle_user_login(self.request.user)
        return response

class HomeView(TemplateView):
    #Specifies what template to use when rendering the view
    template_name = 'home/welcome.html'
