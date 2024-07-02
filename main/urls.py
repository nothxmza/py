from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
	path('', views.home, name='home'),
	path('account/', views.account, name='account'),
	path('settings/', views.settings, name='settings'),
	path('settings/delete/<int:user_id>/', views.delete_user, name='delete_user'),
	path('settings/update/<int:user_id>/', views.update_user, name='update_user'),
	path('student/', views.student_list, name='student_list'),
	path('student/<int:student_id>/', views.student_details, name='student_details'),
	path('instructor/', views.instructor_list, name='instructor_list'),
	path('instructor/<int:instructor_id>', views.instructor_details, name='instructor_details'),

	# path('', views.index, name='index'),
]