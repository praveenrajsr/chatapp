from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chat/', views.chat_box, name="chat"),
    path('login/', views.login),
    path('dashboard/', views.dashboard),
]
