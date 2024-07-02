# planning/models.py
from django.db import models
from django.conf import settings

class Appointment(models.Model):
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_appointments')
	instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_appointments')
	date = models.DateField()
	timeStart = models.TimeField(null=True)
	timeEnd = models.TimeField(null=True)
	location = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.student.username} - {self.date} at {self.timeStart} with {self.instructor.username}"
