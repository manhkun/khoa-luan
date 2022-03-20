from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name='jobs')
]
