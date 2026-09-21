"""LearnSphere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('aboutus',views.aboutUs,name="about"),
    path('courses',views.courses,name="courses"),
    path('display_course',views.display_course,name="display_course"),
    path("login/", views.login, name="login"),
    path('get-registered-users/', views.get_registered_users, name='get_registered_users'),
    path('enroll_login',views.enroll_login,name="enroll_login"),
    path('datascience',views.datascience,name="ds"),
    path('ds1',views.ds1,name="ds1"),
    path('ds2',views.ds2,name="ds2"),
     path('ds3',views.ds3,name="ds3"),
    path('ds4',views.ds4,name="ds4"),

    path('machine',views.machine,name="machine"),
     path('ai1',views.ai1,name="ai1"),
      path('ai2',views.ai2,name="ai2"),
       path('ai3',views.ai3,name="ai3"),


    path('cyber',views.cyber,name="cyber"),
    path('c1',views.c1,name="c1"),
    path('c2',views.c2,name="c2"),
    path('c3',views.c3,name="c3"),


    path('cloud',views.cloud,name="cloud"),
    path('cc1',views.cc1,name="cc1"),
        path('cc2',views.cc2,name="cc2"),
    path('cc3',views.cc3,name="cc3"),
    path('cc4',views.cc4,name="cc4"),

    



    path('devops',views.devops,name="devops"),
    path('do1',views.do1,name="do1"),
    path('do2',views.do2,name="do2"),
    path('do3',views.do3,name="do3"),
    path('do4',views.do4,name="do4"),

    path('web',views.web,name="web"),
    path('w1',views.w1,name="w1"),
    path('w2',views.w2,name="w2"),
    path('w3',views.w3,name="w3"),
    path('w4',views.w4,name="w4"),

    path('dataeng',views.dataeng,name="dataeng"),
    path('de1',views.de1,name="de1"),
    path('de2',views.de2,name="de2"),
    path('de3',views.de3,name="de3"),
    path('de4',views.de4,name="de4"),

    path('mobileapp',views.mobileapp,name="mobileapp"),
    path('app1',views.app1,name="app1"),
    path('app2',views.app2,name="app2"),
    path('app3',views.app3,name="app3"),
    path('app4',views.app4,name="app4"),

    path('blockchain',views.blockchain,name="blockchain"),
    path('b1',views.b1,name="b1"),
    path('b2',views.b2,name="b2"),
    path('b3',views.b3,name="b3"),
    path('b4',views.b4,name="b4"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('Registration',views.register,name="Registration"),
    path('profile-settings/', views.profile_settings, name='profile-settings'),
    path('account-settings/', views.account_settings, name='account-settings'),
    path('nav',views.navigation,name="nav"),
         path("add_quiz/", views.add_quiz, name="add_quiz"),
    path("quiz_<int:quiz_id>_add_questions/", views.add_questions, name="add_questions"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("admin_quizzes/", views.admin_quiz_list, name="admin_quiz_list"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("clear-quiz-session/", views.clear_quiz_session, name="clear_quiz_session"),
    path("quiz/<int:quiz_id>/edit/", views.edit_quiz, name="edit_quiz"),  # ✅ Edit quiz
    path("quiz/<int:quiz_id>/delete/", views.delete_quiz, name="delete_quiz"),  # ✅ Delete quiz
    
    path('studentdash',views.studentdash,name="studentdash"),
    path('stud_nav',views.stud_nav,name="stud_nav"),
    path('stud_announcement',views.stud_announcement,name="stud_announcement"),
    path('assignments/', views.student_assignment_list, name='student_assignment_list'),
  path('edit/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('create/', views.create_assignment, name='create_assignment'),
    path('assignment_list/', views.assignment_list, name='assignment_list'),  # Add the assignment list URL view if you have one
    path('edit_assignment/<int:id>/', views.edit_assignment, name='edit_assignment'),
    path('delete_assignment/<int:id>/', views.delete_assignment, name='delete_assignment'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('create-announcement/', views.create_announcement, name='create_announcement'),
    path('students/', views.student_list, name='student_list'),
    path('edit-profile/', views.edit_student_profile, name='edit_student_profile'),

path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
   path('payment/', views.payment, name='payment'),
   

    path("save_certificate/", views.save_certificate_request, name="save_certificate_request"),

path('certificates/', views.certificate_list, name='certificate_list'),
 

    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),


    path("generate-certificate/<int:quiz_id>/", views.generate_certificate, name="generate_certificate"),

    path('submit-assignment/', views.submit_assignment, name='submit_assignment'),
    
    path('assignments_students/', views.assignment_list_students, name='assignment_list_student'),

   

   ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
