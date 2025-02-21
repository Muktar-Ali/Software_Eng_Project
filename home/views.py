from django.shortcuts import render
from django.http import HttpResponse

#This imports Django's built-in view for rendering templates
from django.views.generic import TemplateView

# Create your views here.
#This view inherits from Templateview
class HomeView(TemplateView):
    #Specifies what template to use when rendering the view
    template_name = 'home/welcome.html'