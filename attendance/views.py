from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.models import Account
from courses.models import Course, ClassSchedule
from attendance.models import Attendance
from datetime import timedelta, date
import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from core.helpers.email_helper import send_absence_warning_email
from django.utils import timezone

@login_required
def attendance_statistic(request, account_id):
    instructor = get_object_or_404(Account, account_id=account_id, role='instructor')
    courses = Course.objects.filter(instructor=instructor)

    statistics_data = [{'course_name': course.course_name, 'course_id': course.course_id} for course in courses]

    context = {
        'instructor': instructor,
        'statistics_data': statistics_data
    }
    return render(request, 'instructor/statistic.html', context)


@login_required
def attendance_statistic_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    start_date = course.start_date
    end_date = course.end_date
    
    weeks = []
    current_date = start_date
    while current_date <= end_date:
        weeks.append(current_date)
        current_date += timedelta(weeks=1)

    students = Account.objects.filter(classschedule__course=course, role='student').distinct()
    student_data = []
    today = date.today()
    
    for student in students:
        weekly_attendance = []
        absent_count = 0
        for week_start in weeks:
            week_end = week_start + timedelta(days=6)
            is_future = week_start > today
            
            attendance = Attendance.objects.filter(
                student=student,
                course=course,
                check_in_date__range=(week_start, week_end)
            ).first()

            if attendance:
                weekly_attendance.append({
                    'details': json.dumps({
                        'check_in_date': attendance.check_in_date.strftime('%Y-%m-%d'),
                        'check_in_time': attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else "N/A",
                        'room': course.room or "N/A"
                    }, ensure_ascii=False),
                    'is_future': is_future
                })
            else:
                weekly_attendance.append({
                    'details': None,
                    'is_future': is_future
                })
                if not is_future:
                    absent_count += 1

        student_data.append({
            'student': student,
            'weekly_attendance': weekly_attendance,
            'absent_count': absent_count,
            'can_warn': absent_count > 3
        })

    context = {
        'course': course,
        'weeks': weeks,
        'student_data': student_data
    }
    return render(request, 'instructor/statistic_detail.html', context)

@login_required
def send_warning_email(request, student_id, course_id):
    student = get_object_or_404(Account, account_id=student_id, role='student')
    course = get_object_or_404(Course, course_id=course_id)
    if send_absence_warning_email(student, course):
        # messages.success(request, f"Đã gửi email cảnh cáo đến {student.full_name}.")
        print("Gui mail thanh cong")
    else:
        # messages.error(request, f"Không thể gửi email cảnh cáo đến {student.full_name}.")
        print("loi gui mail")
    return redirect('attendance:statistic_detail', course_id=course_id)

@login_required
def student_attendance_history(request, account_id):
    student = get_object_or_404(Account, account_id=account_id, role='student')
    # Lấy tất cả các course mà sinh viên tham gia qua ClassSchedule
    courses = Course.objects.filter(classschedule__student=student).distinct()
    today = date.today()
    attendance_data = []
    max_week_count = 0
    for course in courses:
        start_date = course.start_date
        end_date = course.end_date
        # Tạo danh sách ngày bắt đầu của mỗi tuần
        weeks = []
        week_start = start_date
        while week_start <= end_date:
            weeks.append(week_start)
            week_start += timedelta(days=7)
        if len(weeks) > max_week_count:
            max_week_count = len(weeks)
        week_data = []
        for week_start in weeks:
            week_end = week_start + timedelta(days=6)
            is_future = week_start > today
            attendance = Attendance.objects.filter(
                student=student,
                course=course,
                check_in_date__range=(week_start, week_end)
            ).first()
            if attendance:
                week_data.append({
                    'details': json.dumps({
                        'check_in_date': attendance.check_in_date.strftime('%Y-%m-%d'),
                        'check_in_time': attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else "N/A",
                        'room': course.room or "N/A"
                    }, ensure_ascii=False),
                    'is_future': is_future
                })
            else:
                week_data.append({
                    'details': None,
                    'is_future': is_future
                })
        attendance_data.append({
            'course_name': course.course_name,
            'weeks': week_data
        })
    # Tạo list số tuần tối đa để render header
    max_weeks = range(max_week_count)
    context = {
        'student': student,
        'attendance_data': attendance_data,
        'max_weeks': max_weeks
    }
    return render(request, 'student/history.html', context)

