from django.urls import path
from . import views

app_name = 'planning'
urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
	path('add/', views.add_appointment, name='add_appointment'),
	path('add/<int:user_id>/', views.add_appointment, name='add_appointment_with_id'),
	path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
	path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]