from django.contrib.postgres.aggregates import StringAgg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

#cjy开始
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_data = data.get('student')
            applicant_data = data.get('applicant')
            exam_result_data = data.get('examResult')

            # 从 student 对象中获取数据
            studentId = student_data.get('studentId')
            name = student_data.get('name')
            gender = student_data.get('gender')
            major = student_data.get('major')
            school = student_data.get('school')
            phone = student_data.get('phone')
            direction = student_data.get('direction')

            # 打印以验证接收的数据
            print(name, gender, major, school, phone, direction)

            if not all([studentId, name, gender, major, school, phone, direction]):
                return JsonResponse({'message': '所有字段都是必填的'}, status=400)

            try:
                # 保存学生信息
                student = StudentInfo(
                    studentId=studentId,
                    name=name,
                    gender=gender,
                    major=major,
                    school=school,
                    phone=phone,
                    direction=direction
                )
                student.save()

                # 保存申请人信息
                applicant = Applicant(
                    StudentID=applicant_data.get('StudentID'),
                    EnglishScore=applicant_data.get('EnglishScore'),
                    MathScore=applicant_data.get('MathScore'),
                    PoliticScore=applicant_data.get('PoliticScore'),
                    MajorScore=applicant_data.get('MajorScore'),
                )
                applicant.save()

                # 保存考试结果信息
                exam_result = ExamResult(
                    StudentID=exam_result_data.get('StudentID'),
                    WrittenExamScore=exam_result_data.get('WrittenExamScore'),
                    InterviewScore=exam_result_data.get('InterviewScore'),
                )
                exam_result.save()

                return JsonResponse({'message': '学生信息提交成功'}, status=201)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'message': '请求体格式错误'}, status=400)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)


from .serializers import StudentInfoSerializer, ApplicantSerializer, ExamResultSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

class DeleteStudentView(APIView):
    def delete(self, request, student_id):
        # 根据 student_id 查找学生信息
        try:
            student = StudentInfo.objects.get(studentId=student_id)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 删除与学生相关的初试成绩
        Applicant.objects.filter(StudentID=student_id).delete()

        # 删除与学生相关的复试成绩
        ExamResult.objects.filter(StudentID=student_id).delete()

        # 删除学生信息
        student.delete()

        # 返回成功响应
        return Response({'message': '学生信息及其相关数据删除成功'}, status=status.HTTP_200_OK)

class SubmitStudentView(APIView):
    def post(self, request):
        # 打印请求体数据，查看格式
        print("Request Data:", request.data)

        # 获取不同部分的数据
        student_data = request.data.get('student')
        applicant_data = request.data.get('applicant')
        exam_result_data = request.data.get('examResult')

        # 检查数据是否为空
        if not student_data:
            return Response({"error": "Missing student data"}, status=status.HTTP_400_BAD_REQUEST)
        if not applicant_data:
            return Response({"error": "Missing applicant data"}, status=status.HTTP_400_BAD_REQUEST)
        if not exam_result_data:
            return Response({"error": "Missing exam result data"}, status=status.HTTP_400_BAD_REQUEST)

        # 序列化并保存学生信息到 StudentInfo 表
        student_serializer = StudentInfoSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 序列化并保存初试成绩到 Applicant 表
        applicant_serializer = ApplicantSerializer(data=applicant_data)
        if applicant_serializer.is_valid():
            applicant_serializer.save()
        else:
            return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 序列化并保存复试成绩到 ExamResult 表
        exam_result_serializer = ExamResultSerializer(data=exam_result_data)
        if exam_result_serializer.is_valid():
            exam_result_serializer.save()
        else:
            return Response(exam_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': '学生信息提交成功'}, status=status.HTTP_201_CREATED)


class UpdateStudentView(APIView):
    def put(self, request, student_id):
        # 获取学生信息
        try:
            student = StudentInfo.objects.get(studentId=student_id)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 获取初试成绩信息
        try:
            applicant = Applicant.objects.get(StudentID=student_id)
        except Applicant.DoesNotExist:
            return Response({"error": "Applicant data not found"}, status=status.HTTP_404_NOT_FOUND)

        # 获取复试成绩信息
        try:
            exam_result = ExamResult.objects.get(StudentID=student_id)
        except ExamResult.DoesNotExist:
            return Response({"error": "Exam result data not found"}, status=status.HTTP_404_NOT_FOUND)

        # 序列化并更新学生信息
        student_serializer = StudentInfoSerializer(student, data=request.data.get('student'))
        if student_serializer.is_valid():
            student_serializer.save()
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 序列化并更新初试成绩
        applicant_serializer = ApplicantSerializer(applicant, data=request.data.get('applicant'))
        if applicant_serializer.is_valid():
            applicant_serializer.save()
        else:
            return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 序列化并更新复试成绩
        exam_result_serializer = ExamResultSerializer(exam_result, data=request.data.get('examResult'))
        if exam_result_serializer.is_valid():
            exam_result_serializer.save()
        else:
            return Response(exam_result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': '学生信息更新成功'}, status=status.HTTP_200_OK)

class GetStudentChoicesView(APIView):
    def get(self, request, student_id):
        # 根据 student_id 查找学生信息
        try:
            student = StudentInfo.objects.get(studentId=student_id)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 构建志愿选择响应数据
        choices = {
            "firstChoice": student.FirstChoice,
            "secondChoice": student.SecondChoice,
            "thirdChoice": student.ThirdChoice
        }
        print("Returning choices:", choices)

        # 返回成功响应
        return Response(choices, status=status.HTTP_200_OK)

class GetFinalResultView(APIView):
    def get(self, request, student_id):
        # 根据 student_id 查找学生信息
        try:
            student = ExamResult.objects.get(StudentID=student_id)
            print(student)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 构建匹配结果响应数据
        result = {
            "InterviewScore": student.InterviewScore,
            "WrittenScore": student.WrittenExamScore,
            "isAdmitted": student.isadmitted
        }

        # 返回成功响应
        return Response(result, status=status.HTTP_200_OK)
class Getadmission(APIView):
    def get(self, request, student_id):
        # 根据 student_id 查找学生信息
        try:
            student = ExamResult.objects.get(StudentID=student_id)
            print(student)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 构建匹配结果响应数据
        result = {
            "isAdmitted": student.isadmitted
        }
        print(result)
        # 返回成功响应
        return Response(result, status=status.HTTP_200_OK)

from .serializers import TeacherInfoSerializer

class GetMatchResultView(APIView):
    def get(self, request, student_id):
        try:
            student = StudentInfo.objects.get(studentId=student_id)
            print(student)
        except StudentInfo.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # 使用序列化器序列化 TeacherInfo 对象
        serializer = TeacherInfoSerializer(student.FinalTeacher)
        match_result = {
            "FinalTeacher": serializer.data
        }

        return Response(match_result, status=status.HTTP_200_OK)

class StudentInfoView(APIView):
    def get(self, request):
        # 获取学生基本信息、初试成绩和复试成绩
        students = StudentInfo.objects.all()

        student_data = []
        for student in students:
            applicant = Applicant.objects.filter(StudentID=student.studentId).first()
            exam_result = ExamResult.objects.filter(StudentID=student.studentId).first()

            # 假设 TeacherInfo 对象有 name 和 id 属性
            final_teacher_info = {
                'name': student.FinalTeacher.Name,
                'id': student.FinalTeacher.TeacherID
            } if student.FinalTeacher else None

            student_info = {
                'studentId': student.studentId,
                'name': student.name,
                'gender': student.gender,
                'school': student.school,
                'major': student.major,
                'phone': student.phone,
                'direction': student.direction,
                'FirstChoice': student.FirstChoice,
                'SecondChoice': student.SecondChoice,
                'ThirdChoice': student.ThirdChoice,
                'FinalTeacher': final_teacher_info,  # 使用可序列化的格式
                'stage': student.stage,
                'englishScore': applicant.EnglishScore if applicant else None,
                'mathScore': applicant.MathScore if applicant else None,
                'politicScore': applicant.PoliticScore if applicant else None,
                'majorScore': applicant.MajorScore if applicant else None,
                'writtenExamScore': exam_result.WrittenExamScore if exam_result else None,
                'interviewScore': exam_result.InterviewScore if exam_result else None,
                'isAdmitted': student.isadmitted
            }

            student_data.append(student_info)

        return Response(student_data)

from django.db.models import F, FloatField
from django.db.models.functions import Cast


from django.db.models import Window
from django.db.models.functions import RowNumber
def determine_admission_status():
    # 获取所有学生的初试成绩总分
    applicants = Applicant.objects.all().annotate(
        initial_score_total=Cast(F('EnglishScore') + F('MathScore') + F('PoliticScore') + F('MajorScore'),
                                 FloatField())
    )

    # 获取所有学生的复试成绩
    exam_results = ExamResult.objects.all().annotate(
        exam_score_total=Cast(F('WrittenExamScore') + F('InterviewScore'),
                              FloatField())
    )

    # 获取所有学生的信息，包括学科方向
    student_infos = {si.studentId: si.direction for si in StudentInfo.objects.all()}

    # 开始事务
    with transaction.atomic():
        # 计算总分并更新 StudentTotalScore 表
        for applicant in applicants:
            try:
                exam_result = exam_results.get(StudentID=applicant.StudentID)
                final_score = exam_result.exam_score_total
            except ExamResult.DoesNotExist:
                final_score = 0.0

            total_score = (applicant.initial_score_total * 0.6) + (final_score * 0.4)

            # 从 StudentInfo 表中获取 program_name
            program_name = student_infos.get(applicant.StudentID, '')

            # 更新或创建 StudentTotalScore 记录
            StudentTotalScore.objects.update_or_create(
                StudentID=applicant.StudentID,
                defaults={
                    'program_name': program_name,
                    'total_score': total_score,
                }
            )

        # 计算排名
        total_scores = StudentTotalScore.objects.all().annotate(
            student_rank=Window(
                expression=RowNumber(),
                partition_by=[F('program_name')],
                order_by=[F('total_score').desc()]
            )
        )

        # 更新排名
        for score in total_scores:
            StudentTotalScore.objects.filter(StudentID=score.StudentID).update(rank=score.student_rank)

        # 确定录取状态
        programs = Program.objects.all()
        for program in programs:
            students = StudentTotalScore.objects.filter(program_name=program.program_name).order_by('rank')
            for i, student in enumerate(students):
                is_admitted = 1 if i < program.total_recruit else 0
                StudentTotalScore.objects.filter(StudentID=student.StudentID).update(is_admitted=is_admitted)
                StudentInfo.objects.filter(studentId=student.StudentID).update(isadmitted=is_admitted)
                ExamResult.objects.filter(StudentID=student.StudentID).update(isadmitted=is_admitted)


def determine_admission_view(request):
    determine_admission_status()
    return JsonResponse({'status': '录取状态已经决定'})

def student_login(request):
    if request.method == 'POST':
        ID = request.POST.get("StudentID")
        password = request.POST.get("password")
        print("ID:", ID)
        print("Password:", password)

        try:
            people = Studentlogin.objects.get(ID=ID)
            if password == people.password:
                return HttpResponse("y")  # 登录成功
            else:
                return HttpResponse("n")  # 密码错误

        except OtherInfo.DoesNotExist:
            print(2)
            return HttpResponse("n")  # 用户不存在

def mishu_login(request):
    if request.method == 'POST':
        ID = request.POST.get("MishuID")
        password = request.POST.get("password")
        print("ID:", ID)
        print("Password:", password)

        try:
            people = Mishulogin.objects.get(ID=ID)
            if password == people.password:
                return HttpResponse("y")  # 登录成功
            else:
                return HttpResponse("n")  # 密码错误

        except OtherInfo.DoesNotExist:
            print(2)
            return HttpResponse("n")  # 用户不存在

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
@require_http_methods(["GET"])
def get_student_info(request, studentId):
    try:
        student = StudentInfo.objects.get(studentId=studentId)
        applicant = Applicant.objects.get(StudentID=studentId)
        examresult = ExamResult.objects.get(StudentID=studentId)

        result = {
            'studentId': student.studentId,
            'name': student.name,
            'gender': student.gender,
            'major': student.major,
            'school': student.school,
            'phone': student.phone,
            'direction': student.direction,
            'EnglishScore': applicant.EnglishScore,
            'MathScore': applicant.MathScore,
            'PoliticScore': applicant.PoliticScore,
            'MajorScore': applicant.MajorScore,
            'WrittenExamScore': examresult.WrittenExamScore,
            'InterviewScore': examresult.InterviewScore
        }
        return JsonResponse(result)
    except (Student.DoesNotExist, Applicant.DoesNotExist, ExamResult.DoesNotExist):
        return JsonResponse({'error': 'Student not found'}, status=404)

@csrf_exempt
def submit_applicant(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        StudentID = data.get('StudentID')
        EnglishScore = data.get('EnglishScore')
        MathScore = data.get('MathScore')
        PoliticScore = data.get('PoliticScore')
        MajorScore = data.get('MajorScore')

        if not all([StudentID, EnglishScore, MathScore, MajorScore,PoliticScore]):
            return JsonResponse({'message': '所有字段都是必填的'}, status=400)

        try:
            applicant = Applicant(
                StudentID=StudentID,
                EnglishScore=EnglishScore,
                MathScore=MathScore,
                PoliticScore=PoliticScore,
                MajorScore=MajorScore
            )
            applicant.save()
            return JsonResponse({'message': '考生志愿信息提交成功'}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def submit_exam_result(request):
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        StudentID = data.get('StudentID')
        WrittenExamScore = data.get('WrittenExamScore')
        InterviewScore = data.get('InterviewScore')

        # 检查字段是否完整
        if not all([StudentID, WrittenExamScore, InterviewScore]):
            return JsonResponse({'message': '所有字段都是必填的'}, status=400)

        try:
            # 创建并保存新的 ExamResult 实例
            exam_result = ExamResult(
                StudentID=StudentID,
                WrittenExamScore=WrittenExamScore,
                InterviewScore=InterviewScore
            )
            exam_result.save()

            return JsonResponse({'message': '考生复试信息提交成功'}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)

    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def submit_choices(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('studentId')
        first_choice = data.get('firstChoice')
        second_choice = data.get('secondChoice')
        third_choice = data.get('thirdChoice')
        print(student_id, first_choice, second_choice, third_choice)
        # 确保所有字段都有值
        if not student_id or not first_choice or not second_choice or not third_choice:
            return JsonResponse({'success': False, 'message': '所有字段都必须填写'})

        try:
            # 查找学生信息并更新志愿字段
            student = StudentInfo.objects.get(studentId=student_id)
            student.FirstChoice = first_choice
            student.SecondChoice = second_choice
            student.ThirdChoice = third_choice
            student.save()
            return JsonResponse({'success': True, 'message': '志愿提交成功'})
        except StudentInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': '学生信息未找到'})

    return JsonResponse({'success': False, 'message': '无效的请求'})

def submit_all_applications(request):
    if request.method == 'POST':
        # 从请求体中获取JSON数据
        data = json.loads(request.body)

        # 从JSON数据中提取每个志愿的信息
        first_choice = data.get('firstVolunteer')
        second_choice = data.get('secondVolunteer')
        third_choice = data.get('thirdVolunteer')

        # 保存到不同的数据库表中
        Choice1.objects.create(StudentID=first_choice['StudentID'], TeacherID=first_choice['TeacherID'])
        Choice2.objects.create(StudentID=second_choice['StudentID'], TeacherID=second_choice['TeacherID'])
        Choice3.objects.create(StudentID=third_choice['StudentID'], TeacherID=third_choice['TeacherID'])

        return JsonResponse({'message': '所有志愿提交成功'}, status=201)
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

def register(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        e = request.POST.get('email')
        try:
            x = models.User.objects.get(email=e)
            return HttpResponse("n")  # 邮箱已存在
        except models.User.DoesNotExist:
            new_user = models.User.objects.create(username=u, email=e, password=p)
            return HttpResponse("y")  # 用户创建成功
    else:
        # 处理 GET 请求
        return HttpResponse("请使用 POST 请求进行注册。")  # 或者渲染注册表单

def login(request):
    if request.method == 'POST':
        e = request.POST.get('email')
        p = request.POST.get('password')
        try:
            x = models.User.objects.get(email=e)
            if x.password == p:
                return HttpResponse("y")
            else:
                return HttpResponse("n")
        except:
            return HttpResponse("n")
#cjy结束


#lyy开始
from datetime import datetime
import json
import os
import uuid
import time
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import *
from django.db.models import Q
from django.db.models import F
from django.db import transaction
from django.http import JsonResponse

#导师
def teacher_login(request):

    if request.method == 'POST':
        TeacherID = request.POST.get("TeacherID")
        password = request.POST.get("password")
        print("TeacherID:", TeacherID)
        print("Password:", password)

        try:
            teacher = TeacherInfo.objects.get(TeacherID=TeacherID)
            if password == teacher.password:
                return HttpResponse("y")  # 登录成功
            else:
                print(1)
                return HttpResponse("n")  # 密码错误
        except TeacherInfo.DoesNotExist:
            print(2)
            return HttpResponse("n")  # 用户不存在

def get_teacherinfo(request, TeacherID):

        # 根据TeacherID查询导师信息
        teacher = TeacherInfo.objects.get(TeacherID=TeacherID)

        # 根据TeacherID查询所在学科id
        directions_id = DirectionTeacher.objects.filter(teacher_id=TeacherID).values_list('direction_id', flat=True)
        print(directions_id)
        # 根据学科id查询学科名称
        direction_names = ResearchDirection.objects.filter(id__in=directions_id).values_list('direction_name',
                                                                                             flat=True)
        print(direction_names)
        direction_names_str = ",".join(direction_names)

        # 根据所在学科id查询所在专业id
        direction_id = directions_id[0]
        program = ResearchDirection.objects.get(id=direction_id)
        program_id = program.program_id
        # 根据专业id查询专业名称
        program = Program.objects.get(program_id=program_id)
        program_name = program.program_name

        # 根据所在专业id查询所在学院id
        college = Program.objects.get(program_id=program_id)
        college_id = college.college_id
        # 根据学院id查询学院名称
        college = College.objects.get(college_id=college_id)
        college_name = college.college_name

        # 构建返回数据
        data = {
            'TeacherID': teacher.TeacherID,  # id 手动分配
            'Name': teacher.Name,  # 姓名 手动分配
            'Title': teacher.Title,  # 职称 自己填
            'Biography': teacher.Biography,  # 个人简介 自己填
            'Email': teacher.Email,  # 邮箱 自己填
            'Phone': teacher.Phone,  # 电话 自己填
            'AcademicAchievements': teacher.AcademicAchievements,  # 学术成就 可以改
            'Department': college_name,  # 学院 不能改 只读（）
            'Program': program_name,  # 专业 不能改 只读
            'Direction': direction_names_str,  # 学科 不能改 只读
            'EnrollmentQuota': teacher.EnrollmentQuota,  # 指标 不能改 只读
            'QualificationReview': teacher.QualificationReview  # 是否有资格
        }

        # 如果有照片，添加照片URL
        if teacher.Photo:
            data['Photo'] = teacher.Photo.url
            print(teacher.Photo)
            print(teacher.Photo.url)
        else:
            data['Photo'] = None

        return JsonResponse(data)

    # except Exception as e:
    #     return JsonResponse({'error': str(e)})


def update_teacherinfo(request):
    if request.method == 'POST':
        try:
            TeacherID = request.POST.get('TeacherID')
            Name = request.POST.get('Name')
            Title = request.POST.get('Title')
            Biography = request.POST.get('Biography')
            Email = request.POST.get('Email')
            Phone = request.POST.get('Phone')
            AcademicAchievements = request.POST.get('AcademicAchievements')
            Photo = request.FILES.get('Photo')

            teacher = TeacherInfo.objects.get(TeacherID=TeacherID)

            if Photo:
                # 获取原始文件扩展名
                file_extension = os.path.splitext(Photo.name)[1]
                # 生成唯一文件名：时间戳_uuid.扩展名
                unique_filename = f"{int(time.time())}_{str(uuid.uuid4())[:8]}{file_extension}"

                save_path = os.path.join(settings.MEDIA_ROOT, 'teacher_photo')
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                file_path = os.path.join(save_path, unique_filename)

                # 保存文件
                with open(file_path, 'wb+') as destination:
                    for chunk in Photo.chunks():
                        destination.write(chunk)

                Photo = file_path
            else:
                Photo = teacher.Photo

            # 更新教师信息
            TeacherInfo.objects.filter(TeacherID=TeacherID).update(
                Name=Name,
                Title=Title,
                Photo=Photo if Photo else None,
                Biography=Biography,
                Email=Email,
                Phone=Phone,
                AcademicAchievements=AcademicAchievements,
            )

            return HttpResponse("y")

        except Exception as e:
            print("Error:", e)
            return HttpResponse("n")


def show_choice(request, TeacherID,stage):
    try:

        if stage==1:#第一志愿阶段
            student_list = StudentInfo.objects.filter(FirstChoice=TeacherID,isadmitted=1).values(
            'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
           )
        elif stage==2:#第二志愿阶段
            student_list = StudentInfo.objects.filter(SecondChoice=TeacherID,isadmitted=1).values(
                'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        elif stage==3:#第三志愿阶段
            student_list = StudentInfo.objects.filter(ThirdChoice=TeacherID,isadmitted=1).values(
                'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        elif stage==4:  #补选阶段
            student_list = StudentInfo.objects.filter(Q(FinalTeacher=None) | Q(stage__gt=3),isadmitted=1).values(
                'studentId', 'name', 'gender', 'school',  'direction', 'major', 'FinalTeacher'
            )
        else:
            student_list = StudentInfo.objects.filter(Q(FinalTeacher=None),isadmitted=1).values(
                'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )

        # 获取学生的初始成绩和复试成绩
        student_data = []
        for student in student_list:
            student_id = student['studentId']

            # 获取该学生的初始成绩
            initial_score = Applicant.objects.filter(StudentID=student_id).values(
                'EnglishScore', 'MathScore', 'PoliticScore', 'MajorScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            # 获取该学生的复试成绩
            re_exam_score = ExamResult.objects.filter(StudentID=student_id).values(
                'WrittenExamScore', 'InterviewScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            total_score = StudentTotalScore.objects.filter(StudentID=student_id).values(
                'total_score'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            # 将成绩信息合并到学生数据中
            student_info = {
                **student,  # 学生基本信息
                **(initial_score if initial_score else {}),  # 初始成绩（如果存在）
                **(re_exam_score if re_exam_score else {}),  # 复试成绩（如果存在）
                **(total_score if total_score else {}),
            }

            student_data.append(student_info)

        # 以列表形式返回
        return JsonResponse(student_data, safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def sort_student(request,TeacherID,sortField,stage):
    try:
        if stage==1:
            student_list = StudentInfo.objects.filter(FirstChoice=TeacherID,isadmitted=1).values(
              'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        elif stage==2:
            student_list = StudentInfo.objects.filter(SecondChoice=TeacherID,isadmitted=1).values(
              'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        elif stage==3:
            student_list = StudentInfo.objects.filter(ThirdChoice=TeacherID,isadmitted=1).values(
              'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        elif stage == 4:  # 补选阶段
            student_list = StudentInfo.objects.filter(Q(FinalTeacher=None) | Q(stage__gt=3),isadmitted=1).values(
                'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )
        else:
            student_list = StudentInfo.objects.filter(Q(FinalTeacher=None),isadmitted=1).values(
                'studentId', 'name', 'gender', 'school', 'direction', 'major', 'FinalTeacher'
            )


        student_data = []
        for student in student_list:
            student_id = student['studentId']

            # 获取该学生的初始成绩
            initial_score = Applicant.objects.filter(StudentID=student_id).values(
            'EnglishScore', 'MathScore', 'PoliticScore', 'MajorScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            # 获取该学生的复试成绩
            re_exam_score = ExamResult.objects.filter(StudentID=student_id).values(
            'WrittenExamScore', 'InterviewScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            total_score = StudentTotalScore.objects.filter(StudentID=student_id).values(
            'total_score'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

        # 将成绩信息合并到学生数据中
            student_info = {
              **student,  # 学生基本信息
              **(initial_score if initial_score else {}),  # 初始成绩（如果存在）
              **(re_exam_score if re_exam_score else {}),  # 复试成绩（如果存在）
              **(total_score if total_score else {}),
            }

            student_data.append(student_info)

            # 根据sortField进行排序
        if sortField == 'MathScore':
            student_data = sorted(student_data, key=lambda x: x.get('MathScore', 0), reverse=True)  # 按数学成绩升序排序
        elif sortField == 'EnglishScore':
            student_data = sorted(student_data, key=lambda x: x.get('EnglishScore', 0), reverse=True)  # 按英语成绩升序排序
        elif sortField == 'PoliticScore':
            student_data = sorted(student_data, key=lambda x: x.get('PoliticScore', 0), reverse=True)  # 按政治成绩升序排序
        elif sortField == 'MajorScore':
            student_data = sorted(student_data, key=lambda x: x.get('MajorScore', 0), reverse=True)  # 按专业成绩升序排序
        elif sortField == 'WrittenExamScore':
            student_data = sorted(student_data, key=lambda x: x.get('WrittenExamScore', 0),
                                      reverse=True)  # 按笔试成绩升序排序
        elif sortField == 'InterviewScore':
            student_data = sorted(student_data, key=lambda x: x.get('InterviewScore', 0),
                                      reverse=True)  # 按面试成绩升序排序
        elif sortField == 'total_score':
            student_data = sorted(student_data, key=lambda x: x.get('total_score', 0), reverse=True)  # 按总成绩升序排序

        return JsonResponse(student_data, safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def select_student(request,studentId,TeacherID,stage):
    if request.method=='POST':
        try:
            teacher = TeacherInfo.objects.get(TeacherID=TeacherID)
            print(teacher.TeacherID)
            if teacher.Selected < teacher.EnrollmentQuota:
                teacher.Selected += 1  # 导师的剩余指标数减1
                teacher.save()
                StudentInfo.objects.filter(studentId=studentId).update(FinalTeacher=TeacherID,stage=stage)
                return HttpResponse("y")
            else:
                return HttpResponse("n")

        except Exception as e:
            print(e)
            return HttpResponse("n")

def cancel_select(request,studentId,TeacherID):
    if request.method=='POST':
        try:
            teacher = TeacherInfo.objects.get(TeacherID=TeacherID)
            teacher.Selected -= 1  # 导师的剩余指标数加1
            teacher.save()
            StudentInfo.objects.filter(studentId=studentId).update(FinalTeacher=None)
            return HttpResponse("y")
        except Exception as e:
            print(e)
            return HttpResponse("n")



def show_selected_students(request,TeacherID):
    try:
        student_list = StudentInfo.objects.filter(FinalTeacher=TeacherID).values(
            'studentId', 'name', 'gender', 'school', 'phone', 'direction', 'major'
        )
        student_data = []
        for student in student_list:
            student_id = student['studentId']

            # 获取该学生的初始成绩
            initial_score = Applicant.objects.filter(StudentID=student_id).values(
                'EnglishScore', 'MathScore', 'PoliticScore', 'MajorScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            # 获取该学生的复试成绩
            re_exam_score = ExamResult.objects.filter(StudentID=student_id).values(
                'WrittenExamScore', 'InterviewScore'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            total_score = StudentTotalScore.objects.filter(StudentID=student_id).values(
                'total_score'
            ).first()  # 获取第一条记录，假设每个学生只有一条记录

            # 将成绩信息合并到学生数据中
            student_info = {
                **student,  # 学生基本信息
                **(initial_score if initial_score else {}),  # 初始成绩（如果存在）
                **(re_exam_score if re_exam_score else {}),  # 复试成绩（如果存在）
                **(total_score if total_score else {}),
            }

            student_data.append(student_info)

        # 以列表形式返回
        return JsonResponse(student_data, safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def check_stage(request,TeacherID,stage):

    rq = request.GET.get('rq')
    print(rq)
    rq = datetime.strptime(rq, '%Y-%m-%d %H:%M:%S')
    if stage==1:#第一志愿阶段
        try:
            stagetime=StageTime.objects.all().first()
            fb=stagetime.Fbegin
            fe = stagetime.Fend
            if rq>fb and rq<fe:
                return HttpResponse("y")
            else:
                return HttpResponse("n")
        except Exception as e:
            return HttpResponse("n")
    elif stage==2:#第二志愿阶段
        try:
            stagetime=StageTime.objects.all().first()
            sb=stagetime.Sbegin
            se =stagetime.Send
            if rq>sb and rq<se:
                return HttpResponse("y")
            else:
                return HttpResponse("n")
        except Exception as e:
            return HttpResponse("n")
    elif stage == 3:#第三志愿阶段
        try:
            stagetime = StageTime.objects.all().first()
            tb = stagetime.Tbegin
            te = stagetime.Tend
            if rq > tb and rq < te:
                return HttpResponse("y")
            else:
                return HttpResponse("n")
        except Exception as e:
            return HttpResponse("n")

    elif stage==4: #缺额补选
        try:
            additionstage = AdditionStageTime.objects.get(TeacherID=TeacherID)
            ab = additionstage.Abegin
            ae = additionstage.Aend
            if rq > ab and rq < ae:
                return HttpResponse("y")
            else:
                #时间未到
                return HttpResponse("n")

        except Exception as e:
            #无权限
            return HttpResponse("n")
    elif stage==5: #无学生补选
        try:
            additionstage = MissedTeacher.objects.get(TeacherID=TeacherID)
            ab = additionstage.begin
            ae = additionstage.end
            if rq > ab and rq < ae:
                return HttpResponse("y")
            else:
                #时间未到
                return HttpResponse("n")

        except Exception as e:
            #无权限
            return HttpResponse("n")

#学科秘书
def other_login(request):
    if request.method == 'POST':
        ID = request.POST.get("TeacherID")
        password = request.POST.get("password")
        print("ID:", ID)
        print("Password:", password)

        try:
            people = OtherInfo.objects.get(ID=ID)
            if password == people.password:
                return HttpResponse("y")  # 登录成功
            else:
                return HttpResponse("n")  # 密码错误

        except OtherInfo.DoesNotExist:
            print(2)
            return HttpResponse("n")  # 用户不存在

def show_nostudentteacher(request):
    try:
        # 获取所有学生选择的导师（first, second, third列）
        student_choices = StudentInfo.objects.all().values('FirstChoice', 'SecondChoice', 'ThirdChoice')

        # 提取所有导师ID并去重
        teachers = set()
        for choice in student_choices:
            teachers.update([choice['FirstChoice'], choice['SecondChoice'], choice['ThirdChoice']])
        print("所有导师ID")
        print(teachers)

        # 查询未在teachers列表中的导师 即没有学生选择的导师
        missing_teachers = TeacherInfo.objects.exclude(TeacherID__in=teachers)
        print("没有学生选择的导师")
        print(missing_teachers)

        # 获取当前MissedTeacher表中已有的所有TeacherID
        existing_missedteacher_ids = set(MissedTeacher.objects.values_list('TeacherID', flat=True))
        print("旧的没人选的导师")
        print(existing_missedteacher_ids)

        # 创建对象，只插入那些TeacherID不在MissedTeacher表中的导师
        missed_teachers_data = [
            MissedTeacher(TeacherID=teacher.TeacherID, Name=teacher.Name, begin=None,end=None)
            for teacher in missing_teachers if teacher.TeacherID not in existing_missedteacher_ids
        ]
        print("新的没人选的导师")
        print(missed_teachers_data)

        # 如果有新的导师数据需要插入，则批量插入
        if missed_teachers_data:
            print('有')
            with transaction.atomic():  # 使用事务确保数据一致性
                MissedTeacher.objects.bulk_create(missed_teachers_data)
                print('ok')# 批量插入未选择的导师

        # 获取MissedTeacher表中的数据
        teacher_list = MissedTeacher.objects.all().values('TeacherID', 'Name', 'begin', 'end')
        for teacher in teacher_list:
            if teacher['begin'] and teacher['end']:
                teacher['begin'] = teacher['begin'].strftime('%Y-%m-%d %H:%M:%S')
                print(teacher['begin'])
                teacher['end'] = teacher['end'].strftime('%Y-%m-%d %H:%M:%S')
            elif teacher['begin'] is None:
                teacher['begin']=None
            elif teacher['end'] is None:
                teacher['end']=None

        return JsonResponse(list(teacher_list), safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)



def show_lackstudentteacher(request):
    try:
        # 查询Selected小于EnrollmentQuota的所有教师记录
        teachers = TeacherInfo.objects.filter(Selected__lt=F('EnrollmentQuota'))

        # 获取当前AdditionStageTime表中已有的所有TeacherID
        existing_additionteacher_ids = set(AdditionStageTime.objects.values_list('TeacherID', flat=True))

        # 分为两部分处理：已存在的更新，不存在的插入
        update_list = []
        insert_list = []

        for teacher in teachers:
            rest_value = teacher.EnrollmentQuota - teacher.Selected
            if teacher.TeacherID in existing_additionteacher_ids:
                # 如果记录已存在，加入更新列表
                update_list.append({
                    'TeacherID': teacher.TeacherID,
                    'Rest': rest_value,
                })
            else:
                # 如果记录不存在，加入插入列表
                insert_list.append(AdditionStageTime(
                    TeacherID=teacher.TeacherID,
                    Name=teacher.Name,
                    Rest=rest_value,  # 差值字段
                    Abegin=None,
                    Aend=None,
                ))

        # 执行批量更新和插入
        with transaction.atomic():
            # 更新已存在记录的Rest字段
            for update_item in update_list:
                AdditionStageTime.objects.filter(TeacherID=update_item['TeacherID']).update(Rest=update_item['Rest'])

            # 插入不存在的记录
            if insert_list:
                AdditionStageTime.objects.bulk_create(insert_list)

        # 查询更新后的记录并返回
        teacher_list = AdditionStageTime.objects.all().values('TeacherID', 'Name', 'Rest', 'Abegin', 'Aend').order_by('-Rest')
        for teacher in teacher_list:
            if teacher['Abegin'] and teacher['Aend']:
                teacher['Abegin'] = teacher['Abegin'].strftime('%Y-%m-%d %H:%M:%S')
                teacher['Aend'] = teacher['Aend'].strftime('%Y-%m-%d %H:%M:%S')
            elif teacher['Abegin'] is None:
                teacher['Abegin'] = None
            elif teacher['Aend'] is None:
                teacher['Aend'] = None

        return JsonResponse(list(teacher_list), safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


def update_missedteacherinfo(request):
    try:
        TeacherID = request.POST.get('TeacherID')
        print(TeacherID)
        begin = request.POST.get('begin')
        print(begin)
        end = request.POST.get('end')
        TimeType = request.POST.get('TimeType')

        begin = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S') if begin else None
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S') if end else None


        missed_teacher=MissedTeacher.objects.get(TeacherID=TeacherID)
        if TimeType=='begin':
            missed_teacher.begin = begin
        else:
            missed_teacher.end = end
        missed_teacher.save()
        return HttpResponse("y")
    except Exception as e:
        print(e)
        return HttpResponse("n")

def update_lackteacherinfo(request):
    try:
        TeacherID=request.POST.get('TeacherID')
        Abegin=request.POST.get('Abegin')
        Aend=request.POST.get('Aend')
        TimeType=request.POST.get('TimeType')

        Abegin=datetime.strptime(Abegin, '%Y-%m-%d %H:%M:%S') if Abegin else None
        Aend=datetime.strptime(Aend, '%Y-%m-%d %H:%M:%S') if Aend else None

        teacher=AdditionStageTime.objects.get(TeacherID=TeacherID)
        if TimeType=='Abegin':
            teacher.Abegin = Abegin
        else:
            teacher.Aend = Aend
        teacher.save()
        return HttpResponse("y")
    except Exception as e:
        print(e)
        return HttpResponse("n")

def get_stagetime(request):
    try:
        # 根据TeacherID查询导师信息
        stagetime =StageTime.objects.all().first()
        # 构建返回数据
        data = {
            'Fbegin': stagetime.Fbegin.strftime('%Y-%m-%d %H:%M:%S'),
            'Fend': stagetime.Fend.strftime('%Y-%m-%d %H:%M:%S'),
            'Sbegin': stagetime.Sbegin.strftime('%Y-%m-%d %H:%M:%S'),
            'Send': stagetime.Send.strftime('%Y-%m-%d %H:%M:%S'),
            'Tbegin': stagetime.Tbegin.strftime('%Y-%m-%d %H:%M:%S'),
            'Tend': stagetime.Tend.strftime('%Y-%m-%d %H:%M:%S'),
        }
        print(1)
        return JsonResponse(data)

    except Exception as e:
        print(2)
        return JsonResponse({'error': 'n'})

def submit_stagetime(request):

    Fbegin=request.POST.get("Fbegin")
    Sbegin = request.POST.get("Sbegin")
    Tbegin = request.POST.get("Tbegin")
    Fend=request.POST.get("Fend")
    Send = request.POST.get("Send")
    Tend = request.POST.get("Tend")

    Fbegin_datetime = datetime.strptime(Fbegin, '%Y-%m-%d %H:%M:%S') if Fbegin else None
    Sbegin_datetime = datetime.strptime(Sbegin, '%Y-%m-%d %H:%M:%S') if Sbegin else None
    Tbegin_datetime = datetime.strptime(Tbegin, '%Y-%m-%d %H:%M:%S') if Tbegin else None
    Fend_datetime = datetime.strptime(Fend, '%Y-%m-%d %H:%M:%S') if Fend else None
    Send_datetime = datetime.strptime(Send, '%Y-%m-%d %H:%M:%S') if Send else None
    Tend_datetime = datetime.strptime(Tend, '%Y-%m-%d %H:%M:%S') if Tend else None
    print(Fend_datetime)

    try:

        if StageTime.objects.exists():
            StageTime.objects.all().delete()
        print('3')
        stagetime = StageTime(
            Fbegin=Fbegin_datetime,
            Sbegin=Sbegin_datetime,
            Tbegin=Tbegin_datetime,
            Fend=Fend_datetime,
            Send=Send_datetime,
            Tend=Tend_datetime
        )

        stagetime.save()
        return HttpResponse("y")

    except Exception as e:
        print("b")
        return HttpResponse("n")

#lyy结束

#wjx开始
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import College, Program, ResearchDirection, DirectionTeacher, TeacherInfo
from .serializers import CollegeSerializer, ProgramSerializer, ResearchDirectionSerializer, TeacherSerializer, DirectionTeacherSerializer


def xueke_login(request):
    if request.method == 'POST':
        ID = request.POST.get("XueKeID")
        password = request.POST.get("password")
        print("ID:", ID)
        print("Password:", password)

        try:
            people = XueKelogin.objects.get(ID=ID)
            if password == people.password:
                return HttpResponse("y")  # 登录成功
            else:
                return HttpResponse("n")  # 密码错误

        except OtherInfo.DoesNotExist:
            print(2)
            return HttpResponse("n")  # 用户不存在

# 提交学院信息
@api_view(['POST'])
def submit_college(request):
    if request.method == 'POST':
        serializer = CollegeSerializer(data=request.data)

        # 验证数据
        if serializer.is_valid():
            college_id = serializer.validated_data['college_id']
            college_name = serializer.validated_data['college_name']
            total_recruit = serializer.validated_data['total_recruit']

            # 使用 update_or_create 确保数据是更新或创建
            college, created = College.objects.update_or_create(
                college_id=college_id,  # 使用学院ID查找
                defaults={
                    'college_name': college_name,
                    'total_recruit': total_recruit,
                }
            )

            # 返回响应
            if created:
                return JsonResponse({'message': '学院信息已创建', 'college': serializer.data}, status=201)
            else:
                return JsonResponse({'message': '学院信息已更新', 'college': serializer.data}, status=200)

        else:
            return JsonResponse({'message': '无效的数据', 'errors': serializer.errors}, status=400)


# 提交专业信息
@api_view(['POST'])
def submit_program(request):
    if request.method == 'POST':
        serializer = ProgramSerializer(data=request.data)

        # 验证数据
        if serializer.is_valid():
            college_id = request.data.get('college_id')  # 获取学院ID
            program_id = serializer.validated_data['program_id']
            program_name = serializer.validated_data['program_name']
            total_recruit = serializer.validated_data['total_recruit']
            remarks = serializer.validated_data['remarks']

            try:
                # 获取学院对象
                college = College.objects.get(college_id=college_id)

                # 更新或创建专业信息
                program, created = Program.objects.update_or_create(
                    program_id=program_id,  # 使用专业ID查找
                    defaults={
                        'college': college,
                        'program_name': program_name,
                        'total_recruit': total_recruit,
                        'remarks': remarks
                    }
                )

                # 返回响应
                if created:
                    return JsonResponse({'message': '专业信息提交成功'}, status=201)
                else:
                    return JsonResponse({'message': '专业信息更新成功'}, status=200)

            except College.DoesNotExist:
                return JsonResponse({'message': '学院不存在'}, status=400)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': '无效的数据', 'errors': serializer.errors}, status=400)
# 提交研究方向信息
@api_view(['POST'])
def submit_research_direction(request):
    if request.method == 'POST':
        serializer = ResearchDirectionSerializer(data=request.data)

        # 验证数据
        if serializer.is_valid():
            program_id = request.data.get('program_id')  # 获取专业ID
            direction_id = serializer.validated_data['direction_id']
            direction_name = serializer.validated_data['direction_name']
            exam_subjects = serializer.validated_data['exam_subjects']

            try:
                # 获取对应的专业
                program = Program.objects.get(program_id=program_id)

                # 检查研究方向是否已经存在
                if ResearchDirection.objects.filter(program=program, direction_id=direction_id).exists():
                    return JsonResponse({'message': '该研究方向已存在，无法更新'}, status=400)

                # 创建新的研究方向记录
                research_direction = ResearchDirection.objects.create(
                    program=program,
                    direction_id=direction_id,
                    direction_name=direction_name,
                    exam_subjects=exam_subjects
                )

                return JsonResponse({'message': '研究方向信息提交成功'}, status=201)

            except Program.DoesNotExist:
                return JsonResponse({'message': '专业不存在'}, status=400)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': '无效的数据', 'errors': serializer.errors}, status=400)

# 提交研究方向与导师的关联
@api_view(['POST'])
def submit_direction_teacher(request):
    if request.method == 'POST':
        serializer = DirectionTeacherSerializer(data=request.data)

        # 验证数据
        if serializer.is_valid():
            # 提交或更新研究方向与导师的关联数据
            direction_id = request.data.get('direction_id')
            teacher_id = request.data.get('tutor_id')

            try:
                direction = ResearchDirection.objects.get(id=direction_id)
                teacher = TeacherInfo.objects.get(TeacherID=teacher_id)

                # 创建或更新 DirectionTeacher 关联
                direction_teacher, created = DirectionTeacher.objects.update_or_create(
                    direction=direction,
                    teacher=teacher
                )

                if created:
                    return JsonResponse({'message': '研究方向与导师的关联信息提交成功'}, status=201)
                else:
                    return JsonResponse({'message': '研究方向与导师的关联信息更新成功'}, status=200)
            except ResearchDirection.DoesNotExist:
                return JsonResponse({'message': '研究方向不存在'}, status=400)
            except TeacherInfo.DoesNotExist:
                return JsonResponse({'message': '导师不存在'}, status=400)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': '无效的数据', 'errors': serializer.errors}, status=400)
@api_view(['GET'])
def get_all_colleges(request):
    colleges = College.objects.all()  # 获取所有 College 对象
    serializer = CollegeSerializer(colleges, many=True)  # 序列化数据
    return Response(serializer.data)  # 返回 JSON 格式的数据

@api_view(['GET'])
def get_programs_by_college(request, college_id):
    try:
        # 获取指定学院的专业方向
        college = College.objects.get(college_id=college_id)
        programs = college.programs.all()  # 通过 related_name 访问学院下的所有专业方向
        serializer = ProgramSerializer(programs, many=True)  # 序列化数据
        return Response(serializer.data)  # 返回 JSON 格式的数据
    except College.DoesNotExist:
        return Response({'message': '学院不存在'}, status=404)


@api_view(['GET'])
def get_research_directions(request, program_id):
    try:
        # 获取对应的专业
        program = Program.objects.get(program_id=program_id)
        # 获取该专业下所有研究方向
        research_directions = ResearchDirection.objects.filter(program=program)

        # 序列化研究方向数据
        serializer = ResearchDirectionSerializer(research_directions, many=True)

        return Response(serializer.data)

    except Program.DoesNotExist:
        return Response({'message': '该专业不存在'}, status=404)

@api_view(['GET'])
def get_directions_teacher(request, directionId):
    try:
        # 获取对应的研究方向
        direction = ResearchDirection.objects.get(id=directionId)

        # 获取该研究方向下所有导师
        directions_teachers = DirectionTeacher.objects.filter(direction=direction)

        # 序列化数据并返回
        serializer = DirectionTeacherSerializer(directions_teachers, many=True)

        return Response(serializer.data)

    except ResearchDirection.DoesNotExist:
        return Response({'message': '该研究方向不存在'}, status=404)


# 删除学院信息（级联删除相关专业、研究方向、方向教师）
@api_view(['DELETE'])
def delete_college(request, college_id):
    try:
        # 查找学院
        college = College.objects.get(college_id=college_id)

        # 删除学院及其相关联的所有专业、研究方向和方向教师
        college.delete()

        return JsonResponse({'message': '学院及其相关信息已删除'}, status=200)
    except College.DoesNotExist:
        return JsonResponse({'message': '学院不存在'}, status=404)


# 删除专业信息（级联删除相关研究方向、方向教师）
@api_view(['DELETE'])
def delete_program(request, program_id):
    try:
        # 查找专业
        program = Program.objects.get(program_id=program_id)

        # 删除专业及其相关联的所有研究方向和方向教师
        program.delete()

        return JsonResponse({'message': '专业及其相关信息已删除'}, status=200)
    except Program.DoesNotExist:
        return JsonResponse({'message': '专业不存在'}, status=404)


# 删除研究方向信息（级联删除相关方向教师）
@api_view(['DELETE'])
def delete_research_direction(request, id):
    try:
        # 查找研究方向
        research_direction = ResearchDirection.objects.get(id=id)

        # 删除研究方向及其相关联的方向教师
        research_direction.delete()

        return JsonResponse({'message': '研究方向及其相关方向教师已删除'}, status=200)
    except ResearchDirection.DoesNotExist:
        return JsonResponse({'message': '研究方向不存在'}, status=404)



# 删除研究方向与导师的关联
@api_view(['DELETE'])
def delete_direction_teacher(request, directionId, teacherId):
    try:
        # 查找研究方向和导师
        direction = ResearchDirection.objects.get(id=directionId)
        teacher = TeacherInfo.objects.get(TeacherID=teacherId)

        # 查找方向与导师的关联并删除
        direction_teacher = DirectionTeacher.objects.get(direction=direction, teacher=teacher)
        direction_teacher.delete()

        return JsonResponse({'message': '研究方向与导师的关联已删除'}, status=200)
    except ResearchDirection.DoesNotExist:
        return JsonResponse({'message': '研究方向不存在'}, status=404)
    except TeacherInfo.DoesNotExist:
        return JsonResponse({'message': '导师不存在'}, status=404)
    except DirectionTeacher.DoesNotExist:
        return JsonResponse({'message': '该研究方向与导师关联不存在'}, status=404)


# 修改学院信息
@api_view(['PUT'])
def update_college(request, college_id):
    try:
        # 获取学院对象
        college = College.objects.get(college_id=college_id)

        # 使用序列化器更新学院信息
        serializer = CollegeSerializer(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': '学院信息已更新', 'data': serializer.data}, status=200)
        return JsonResponse({'message': '更新失败', 'errors': serializer.errors}, status=400)
    except College.DoesNotExist:
        return JsonResponse({'message': '学院不存在'}, status=404)


    serializer = CollegeSerializer(data=request.data)

    # 验证数据
    if serializer.is_valid():
        college_id = serializer.validated_data['college_id']
        college_name = serializer.validated_data['college_name']
        total_recruit = serializer.validated_data['total_recruit']

        # 使用 update_or_create 确保数据是更新或创建
        college, created = College.objects.update_or_create(
            college_id=college_id,  # 使用学院ID查找
            defaults={
                'college_name': college_name,
                'total_recruit': total_recruit,
            }
        )

# 修改专业信息
@api_view(['PUT'])
def update_program(request, program_id):
    try:
        # 获取专业对象
        program = Program.objects.get(program_id=program_id)
        # 使用序列化器更新专业信息
        serializer = ProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': '专业信息已更新', 'data': serializer.data}, status=200)
        return JsonResponse({'message': '更新失败', 'errors': serializer.errors}, status=400)
    except Program.DoesNotExist:
        return JsonResponse({'message': '专业不存在'}, status=404)


# 修改研究方向信息
@api_view(['PUT'])
def update_research_direction(request, id):
    try:
        # 获取研究方向对象
        research_direction = ResearchDirection.objects.get(id=id)

        # 使用序列化器更新研究方向信息
        serializer = ResearchDirectionSerializer(research_direction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': '研究方向信息已更新', 'data': serializer.data}, status=200)
        return JsonResponse({'message': '更新失败', 'errors': serializer.errors}, status=400)
    except ResearchDirection.DoesNotExist:
        return JsonResponse({'message': '研究方向不存在'}, status=404)


# 修改研究方向与导师的关联
@api_view(['PUT'])
def update_direction_teacher(request, directionId, teacher_id):
    try:
        # 获取方向与导师关联对象
        direction_teacher = DirectionTeacher.objects.get(direction__id=directionId,
                                                         teacher__TeacherID=teacher_id)

        # 使用序列化器更新关联信息
        serializer = DirectionTeacherSerializer(direction_teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': '研究方向与导师的关联已更新', 'data': serializer.data}, status=200)
        return JsonResponse({'message': '更新失败', 'errors': serializer.errors}, status=400)
    except DirectionTeacher.DoesNotExist:
        return JsonResponse({'message': '该研究方向与导师关联不存在'}, status=404)

def get_tutorinfo(request, TeacherID):

    try:
        # 根据TeacherID查询导师信息
        teacher = TeacherInfo.objects.get(TeacherID=TeacherID)

        # 构建返回数据
        data = {
            'TeacherID': teacher.TeacherID,
            'Name': teacher.Name,
            'Title': teacher.Title,
            'Biography': teacher.Biography,
            'Email': teacher.Email,
            'Phone': teacher.Phone,
            'Department': teacher.Department,
            'AcademicAchievements': teacher.AcademicAchievements,
            'EnrollmentQuota': teacher.EnrollmentQuota,
        }

        # 如果有照片，添加照片URL
        if teacher.Photo:
            data['Photo'] = teacher.Photo.url
            print(teacher.Photo)
            print(teacher.Photo.url)
        else:
            data['Photo'] = None

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)})

def update_teacherinfo2(request):
    if request.method == 'POST':
        try:
            TeacherID = request.POST.get('TeacherID')
            Name = request.POST.get('Name')
            Title = request.POST.get('Title')
            Biography = request.POST.get('Biography')
            Email = request.POST.get('Email')
            Phone = request.POST.get('Phone')
            AcademicAchievements = request.POST.get('AcademicAchievements')
            Photo = request.FILES.get('Photo')
            QualificationReview = request.POST.get('QualificationReview')
            EnrollmentQuota = request.POST.get('EnrollmentQuota')
            teacher = TeacherInfo.objects.get(TeacherID=TeacherID)
            if Photo:
                # 获取原始文件扩展名
                file_extension = os.path.splitext(Photo.name)[1]
                # 生成唯一文件名：时间戳_uuid.扩展名
                unique_filename = f"{int(time.time())}_{str(uuid.uuid4())[:8]}{file_extension}"

                save_path=os.path.join(settings.MEDIA_ROOT,'teacher_photo')
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                file_path=os.path.join(save_path,unique_filename)

                #保存文件
                with open(file_path, 'wb+') as destination:
                    for chunk in Photo.chunks():
                        destination.write(chunk)

                Photo=file_path
            else:
                Photo = teacher.Photo

            # 更新教师信息
            TeacherInfo.objects.filter(TeacherID=TeacherID).update(
                Name=Name,
                Title=Title,
                Photo=Photo if Photo else None,
                Biography=Biography,
                Email=Email,
                Phone=Phone,
                AcademicAchievements=AcademicAchievements,
                EnrollmentQuota = EnrollmentQuota,
                QualificationReview =QualificationReview
            )

            return HttpResponse("y")

        except Exception as e:
            print("Error:", e)
            return HttpResponse("n")



@api_view(['GET'])
def students_grouped_by_teacher(request):
    try:
        # 获取所有导师信息
        teacher_list = TeacherInfo.objects.all().values('TeacherID', 'Name')  # 假设你有TeacherID和TeacherName

        teacher_data = []

        # 遍历每个导师，获取该导师的学生信息
        for teacher in teacher_list:
            teacher_id = teacher['TeacherID']
            teacher_name = teacher['Name']

            # 获取该导师的所有学生信息
            student_list = StudentInfo.objects.filter(FinalTeacher=teacher_id).values(
                'studentId', 'name', 'gender', 'school', 'phone', 'direction', 'major'
            )

            student_data = []
            for student in student_list:
                student_id = student['studentId']

                # 获取该学生的初始成绩
                initial_score = Applicant.objects.filter(StudentID=student_id).values(
                    'EnglishScore', 'MathScore', 'PoliticScore', 'MajorScore'
                ).first()  # 获取第一条记录，假设每个学生只有一条记录

                # 获取该学生的复试成绩
                re_exam_score = ExamResult.objects.filter(StudentID=student_id).values(
                    'WrittenExamScore', 'InterviewScore'
                ).first()  # 获取第一条记录，假设每个学生只有一条记录

                # 获取该学生的总成绩
                total_score = StudentTotalScore.objects.filter(StudentID=student_id).values(
                    'total_score'
                ).first()  # 获取第一条记录，假设每个学生只有一条记录

                # 合并学生基本信息和成绩信息
                student_info = {
                    **student,  # 学生基本信息
                    **(initial_score if initial_score else {}),  # 初始成绩（如果存在）
                    **(re_exam_score if re_exam_score else {}),  # 复试成绩（如果存在）
                    **(total_score if total_score else {}),
                }

                student_data.append(student_info)

            # 将该导师的学生数据添加到返回的数据中
            teacher_info = {
                'TeacherID': teacher_id,
                'TeacherName': teacher_name,
                'Students': student_data
            }
            teacher_data.append(teacher_info)

        # 以列表形式返回所有导师及其学生信息
        return JsonResponse(teacher_data, safe=False)

    except Exception as e:
        print(f"查询错误: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def get_tutors_from_view(request):
    """
    从 TeacherNameView 视图获取导师列表
    """
    if request.method == 'GET':
        # 获取查询集并转换为列表
        tutors = list(TeacherNameView.objects.all().values('TeacherID', 'Name'))
        # 返回正确格式的 JSON 数据
        return JsonResponse({'tutors': tutors}, status=200)
    else:
        # 非 GET 请求的错误响应
        return JsonResponse({'error': 'Invalid request method'}, status=405)