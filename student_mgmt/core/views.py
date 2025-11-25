from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import StudentProfile, Course, Enrollment, Attendance
from .serializers import (
    StudentProfileSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    AttendanceSerializer
)
from .permissions import IsAdmin, IsTeacher, IsTeacherOrAdmin, IsStudent


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Only admin can create or delete student profiles
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdmin]

        # Admin & teacher can update student info
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdmin, IsTeacher]

        else:
            # Students can view only their profile; admin/teacher can view all
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('teacher').all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmin]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacherOrAdmin]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('enrollment').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrAdmin]
