from .views import Home, Home,Pickle, diabetes_pre
from django.urls import path

urlpatterns = [
    path('pickle',Pickle,name='Pickle'),
    path('diabetes_pre/', diabetes_pre, name='diabetesprediction'),
    path('home',Home),
]