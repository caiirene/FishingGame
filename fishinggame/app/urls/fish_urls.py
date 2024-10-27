from django.urls import path
from .. import views

urlpatterns = [
    path('catch/', views.fish_catch, name='fish_catch'),
    path('sell/', views.fish_sell, name='fish_sell'),
]
