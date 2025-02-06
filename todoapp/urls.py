from django.urls import path
from todoapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('add_task/', views.add_task, name='add_task'),
    # path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    # path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
]
