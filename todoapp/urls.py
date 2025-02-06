from django.urls import path
from todoapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_register, name='user_register'),
]
