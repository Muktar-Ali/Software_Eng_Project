#importing path
from django.urls import path
#importing views from current app
from . import views 

urlpatterns = [
    #This maps the root URL to the HomeView
    #The .as_view() method is needed to convert the view into a usable function
    #reverse URL lookups in templates and views are allowed because of name='home'
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
]