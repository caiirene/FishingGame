from django.urls import path
from .. import views

urlpatterns = [
    path('is-exist/', views.user_exist, name='user_exist'),
    path('basic/', views.user_basic, name='user_basic'),
    path('finance/', views.user_finance, name='user_finance'),
    path('level/', views.user_level, name='user_level'),
    path('inventory/', views.user_inventory, name='user_inventory'),
    path('achievement/', views.user_achievement, name='user_achievement'),
    path('create/', views.user_create, name='user_create'),
    path('generate-token/', views.generate_token, name='generate_token'),
]