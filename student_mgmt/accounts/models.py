from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT
