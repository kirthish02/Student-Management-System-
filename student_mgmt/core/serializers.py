from rest_framework import serializers
from .models import StudentProfile, Course, Enrollment, Attendance
from accounts.serializers import UserSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'roll_no', 'phone', 'dob')


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=None, source='teacher', write_only=True, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # avoid circular import at runtime
        from django.contrib.auth import get_user_model
        self.fields['teacher_id'].queryset = get_user_model().objects.filter(role='teacher')

    class Meta:
        model = Course
        fields = ('id', 'title', 'code', 'description', 'teacher', 'teacher_id')


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=None, source='student', write_only=True
    )
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import StudentProfile
        self.fields['student_id'].queryset = StudentProfile.objects.all()

    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'student_id', 'course', 'course_id', 'enrolled_on')
        read_only_fields = ('enrolled_on',)


class AttendanceSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer(read_only=True)
    enrollment_id = serializers.PrimaryKeyRelatedField(
        queryset=Enrollment.objects.all(), source='enrollment', write_only=True
    )

    class Meta:
        model = Attendance
        fields = ('id', 'enrollment', 'enrollment_id', 'date', 'present', 'remarks')
