from .models import StudentInfo, Applicant, ExamResult
from rest_framework import serializers
from .models import College, Program, ResearchDirection, TeacherInfo, DirectionTeacher

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = '__all__'

    # 确保可选字段不会被强制验证
    FirstChoice = serializers.CharField(required=False, allow_null=True)
    SecondChoice = serializers.CharField(required=False, allow_null=True)
    ThirdChoice = serializers.CharField(required=False, allow_null=True)
    FinalTeacher = serializers.CharField(required=False, allow_null=True)
    stage = serializers.IntegerField(required=False, allow_null=True)

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'



class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_id', 'college_name', 'total_recruit']  # 所有需要返回的字段
class ProgramSerializer(serializers.ModelSerializer):
    college = CollegeSerializer(read_only=True)  # 嵌套学院信息

    class Meta:
        model = Program
        fields = ['college', 'program_id', 'program_name', 'total_recruit', 'remarks']

class ResearchDirectionSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)  # 嵌套专业信息
    class Meta:
        model = ResearchDirection
        fields = ['id', 'program', 'direction_id', 'direction_name', 'exam_subjects']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherInfo
        fields = ['TeacherID', 'Name', 'Title', 'Email', 'Phone']

class DirectionTeacherSerializer(serializers.ModelSerializer):
    direction = ResearchDirectionSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = DirectionTeacher
        fields = ['id', 'direction', 'teacher']

from rest_framework import serializers

class TeacherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherInfo
        fields = '__all__'  # 或者指定需要的字段