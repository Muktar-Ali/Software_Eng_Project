#importing path
from django.urls import path
#importing views from current app
from . import views 

urlpatterns = [
    #This maps the root URL to the HomeView
    #The .as_view() method is needed to convert the view into a usable function
    #reverse URL lookups in templates and views are allowed because of name='home'
    path('main', views.UserMainView.as_view(), name='users.main'),
]