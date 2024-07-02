from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
		('secretary', 'Secretary'),
        ('admin', 'Admin'),
    ]

    roles = models.CharField(max_length=50, choices=ROLES_CHOICES, null=True, blank=True)
    hours_paid = models.IntegerField(default=0)
    hours_taken = models.IntegerField(default=0)