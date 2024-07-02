from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, loginCustom, logoutCustom

app_name = 'auth'
urlpatterns = [
    path('login/', loginCustom, name='login'),
    path('logout/', logoutCustom, name='logout'),
    path('register/', register, name='register'),
]