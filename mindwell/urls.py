# urls.py

from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # URL patterns for the mindwell app
    # path('', HomePageView.as_view(), name='home'),
    ]