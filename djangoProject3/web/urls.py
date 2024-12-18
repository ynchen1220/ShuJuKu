from django.urls import  path, include
from django.conf.urls.static import static

from django.conf import settings
from . import views
from .views import StudentInfoView, SubmitStudentView, DeleteStudentView, UpdateStudentView, GetMatchResultView, \
    GetStudentChoicesView, GetFinalResultView, Getadmission

urlpatterns = [
   #cjy开始
    path('submit-student/', views.submit_student, name='submit-student'),
    path('submit-applicant/', views.submit_applicant, name='submit-applicant'),
    path('submit-exam-result/', views.submit_exam_result, name='submit_exam_result'),
    path('submit_all_applications/', views.submit_all_applications, name='submit_all_applications'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('studentlogin/', views.student_login, name='student_login'),
    path('mishulogin/', views.mishu_login, name='mishu_login'),
    path('get_student_info/<str:studentId>/', views.get_student_info, name='get_student_info'),
    path('submit-choices/', views.submit_choices, name='submit-choices'),
    path('student-info/', StudentInfoView.as_view(), name='student_info'),
    path('submit-student/', SubmitStudentView.as_view(), name='submit-student'),
    path('delete-student/<str:student_id>/', DeleteStudentView.as_view(), name='delete-student'),
    path('update-student/<str:student_id>/', UpdateStudentView.as_view(), name='update-student'),
    path('get_match_result/<str:student_id>/', GetMatchResultView.as_view(), name='get-match-result'),
    path('get-student-choices/<str:student_id>/', GetStudentChoicesView.as_view(), name='get-student-choices'),
    path('get_retest_scores/<str:student_id>/', GetFinalResultView.as_view(), name='get_retest_scores'),
    path('get_admission_status/<str:student_id>/', Getadmission.as_view(), name='get_admission_status'),
    # path('calculate_scores/',views.calculate_scores,name='calculate_scores'),
    # path('rank_students_view/',views.rank_students_view,name='rank_students_view'),
    path('determine_admission_view/',views.determine_admission_view,name='determine_admission_view'),
    #cjy结束


    # lyy开始
    #导师
    path('updateteacherinfo/', views.update_teacherinfo),
    path('getteacherinfo/<str:TeacherID>/', views.get_teacherinfo),
    path('teacherlogin/', views.teacher_login, name='teacher_login'),
    path('showchoice/<str:TeacherID>/<int:stage>', views.show_choice),
    path('selectstudent/<str:studentId>/<str:TeacherID>/<str:stage>', views.select_student),
    path('cancelselect/<str:studentId>/<str:TeacherID>', views.cancel_select),
    path('showselectedstudents/<str:TeacherID>/', views.show_selected_students),
    path('checkstage/<str:TeacherID>/<int:stage>/', views.check_stage),
    path('sortstudents/<str:TeacherID>/<str:sortField>/<int:stage>', views.sort_student),
    #学科秘书
    path('otherlogin/', views.other_login),
    path('getstagetime/', views.get_stagetime),
    path('submitstagetime/', views.submit_stagetime),
    path('shownostudentteacher/', views.show_nostudentteacher),
    path('updateteachertime/', views.update_missedteacherinfo),
    path('showlackstudentteacher/', views.show_lackstudentteacher),
    path('updatelackteachertime/', views.update_lackteacherinfo),
    # lyy结束

    #wjx
    path('gettutorsfromview/', views.get_tutors_from_view),
    path('updateteacherinfo2/', views.update_teacherinfo2),
    path('gettutorinfo/<str:TeacherID>/', views.get_tutorinfo),
    path('xuekelogin/', views.xueke_login, name='xueke_login'),
    path('submit-college/', views.submit_college, name='submit-college'),
    path('submit-program/', views.submit_program, name='submit-program'),
    path('submit-research-direction/', views.submit_research_direction, name='submit-research-direction'),
    path('submit-direction-tutor/', views.submit_direction_teacher, name='submit-directio-teacher'),
    path('colleges/', views.get_all_colleges, name='get-all-colleges'),
    path('colleges/<str:college_id>/programs/', views.get_programs_by_college, name='get-programs-by-college'),
    path('colleges/programs/<str:program_id>/directions/', views.get_research_directions, name='get-research-directions'),
    path('colleges/programs/directions/<str:directionId>/teachers/', views.get_directions_teacher, name='get-directions-teacher'),

    path('delete-college/<str:college_id>/', views.delete_college, name='delete_college'),
    path('delete-program/<str:program_id>/', views.delete_program, name='delete_program'),
    path('delete-research-direction/<str:id>/', views.delete_research_direction, name='delete_research_direction'),
    path('delete-direction-teacher/<str:directionId>/<str:teacherId>/', views.delete_direction_teacher, name='delete_direction_teacher'),
    path('update-college/<str:college_id>/', views.update_college, name='update_college'),
    path('update-program/<str:program_id>/', views.update_program, name='update_program'),
    path('update-research-direction/<str:id>/', views.update_research_direction, name='update_research_direction'),
    path('teacher-student-list/', views.students_grouped_by_teacher, name='students-grouped-by-teacher'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)