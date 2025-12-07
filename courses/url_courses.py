from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signIn, name='login'),
    path('logout/', views.SignOut, name='logout'),
    path('courses/', views.view_courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll_course/',views.enroll_course,name='enroll_course'),
]
