from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class UserMainView(LoginRequiredMixin, TemplateView):
    #Specifies what template to use when rendering the view
    template_name = 'users/main.html'
    login_url = '/login'
