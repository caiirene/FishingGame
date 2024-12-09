from django.urls import path
from .. import views
from ..views import CreateFishView

urlpatterns = [
    path('catch/', views.fish_catch, name='fish_catch'),
    path('sell/', views.fish_sell, name='fish_sell'),
    path('api/create-fish/', CreateFishView.as_view(), name='create-fish'),
]
