"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('signup/', views.signupuser,name='signupuser'),
    path('login/', views.loginuser,name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    path('student/', views.student,name='student'),
    path('studentInfo/', views.studentInfo,name='studentInfo'),
    path('exam_schedule/', views.exam_schedule,name='exam_schedule'),
    path('studentInfo/<str:pk>', views.studentInfoupdate,name='studentInfoupdate'),
    path('seat_plan/', views.seat_plan,name='seat_plan'),


    path('faculty/', views.faculty,name='faculty'),

    path('admin_panel/', views.admin_panel,name='admin_panel'),
    path('room_create/', views.room_create,name='room_create'),
    path('room_restore/', views.room_restore,name='room_restore'),
    path('room_update/<str:pk>', views.room_update,name='room_update'),
    path('room_delete/<str:pk>', views.room_delete,name='room_delete'),
    path('room/<str:pk>', views.room,name='room'),
    path('seat_manage/', views.seat_manage,name='seat_manage'),
    path('delete_seat/', views.delete_seat,name='delete_seat'),

    path('schedule_create/', views.schedule_create,name='schedule_create'),
    path('date_view/', views.date_view,name='date_view'),
    path('date_delete/<str:pk>', views.date_delete,name='date_delete'),


    path('exam/', views.exam,name='exam'),
    path('delete_date/', views.delete_date,name='delete_date'),
    path('exam_create/', views.exam_create,name='exam_create'),
    path('exam_update/<str:pk>', views.exam_update,name='exam_update'),
    path('exam_delete/<str:pk>', views.exam_delete,name='exam_delete'),

]
