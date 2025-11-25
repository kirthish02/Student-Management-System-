from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_no = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.roll_no})"


class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"


class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('enrollment', 'date')

    def __str__(self):
        return f"{self.enrollment.student} - {self.date} - {'P' if self.present else 'A'}"
