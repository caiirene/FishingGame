from django.urls import path
from .. import views

urlpatterns = [
    path('general/', views.chat_general, name='chat_general'),
    path('command/', views.chat_command, name='chat_command'),
    path('draw/', views.chat_draw, name='chat_draw'),
]


from django.urls import path
from app.chat_openai_view import ChatGeneralView, ChatCommandView, ChatDrawView

urlpatterns = [
    path('general/', ChatGeneralView.as_view(), name='chat_general'),
    path('command/', ChatCommandView.as_view(), name='chat_command'),
    path('draw/', ChatDrawView.as_view(), name='chat_draw'),
]
