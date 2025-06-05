from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('statistic/<str:account_id>/', views.attendance_statistic, name='statistic'),
    path('statistic-detail/<str:course_id>/', views.attendance_statistic_detail, name='statistic_detail'),
    path('send-warning/<str:student_id>/<str:course_id>/', views.send_warning_email, name='send_warning_email'),
    path('history/<str:account_id>/', views.student_attendance_history, name='history'),
]