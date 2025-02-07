from django.urls import path
from todoapp import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:reset_code>/', views.reset_password, name='reset_password'),


    path('', views.home, name='home'),
    path('add_task/', views.add_task, name='add_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

    path('add-category/', views.add_category, name='add_category'),
    path('category_list', views.category_list, name='category_list'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),


   
]
