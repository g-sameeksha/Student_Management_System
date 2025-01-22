from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm
from django.contrib import messages
from .models import Staff,Course,SessionYear,Subject,Student,AdminHOD,Attendence,AttendenceReport
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.contrib.sessions import serializers
from django.core import serializers
import json
from django.db import transaction


def staff_home(request):
    return render(request,"staff_template/staff_home.html")

def staff_take_attendence(request):
    staff = Staff.objects.get(admin =request.user)
    subjects = Subject.objects.filter(staff_id = staff.id)
    session_years = SessionYear.objects.all()
    return render(request,"staff_template/staff_take_attendence.html",{"subjects":subjects,"session_years":session_years})


@csrf_exempt
def get_students(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        session_id = request.POST.get("session_year")

        # Debugging inputs
        print(f"Subject ID: {subject_id}, Session ID: {session_id}")

        # Validate inputs
        if not subject_id or not session_id:
            return JsonResponse({"error": "Subject or Session Year is missing"}, status=400)

        try:
            subject_id = int(subject_id)
            session_id = int(session_id)
        except ValueError:
            return JsonResponse({"error": "Invalid Subject or Session Year ID"}, status=400)

        try:
            # Fetch subject and session year
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

        try:
            session_model = SessionYear.objects.get(id=session_id)
        except SessionYear.DoesNotExist:
            return JsonResponse({"error": "Session Year not found"}, status=404)

        # Query students
        students = Student.objects.filter(
            course_id=subject.course_id, session_year_id=session_model.id
        )

        # Serialize student data
        # students_data = serializers.serialize("python",students) # Adjust fields as necessary
        list_data = []
        for student in students:
            data_small = {"id":student.admin.id,"name":student.admin.first_name +" "+student.admin.last_name }
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type ="application/json",safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def save_attendance_data(request):
    if request.method == "POST":
        # Get data from the POST request
        student_ids_json = request.POST.get("student_ids")  # Getting the student_ids as a JSON string
        subject_id = request.POST.get("subject_id")
        attendence_date = request.POST.get("attendence_date")
        session_year_id = request.POST.get("session_year_id")

        try:
            student_ids = json.loads(student_ids_json)
            subject_model = Subject.objects.get(id=subject_id)
            session_model = SessionYear.objects.get(id=session_year_id)
            attendence = Attendence(subject_id=subject_model, attendence_date=attendence_date, session_year_id=session_model)
            attendence.save()
            print(f"Attendence ID: {attendence.id}")

            with transaction.atomic():

                for student_id in student_ids:
        
                        student = Student.objects.get(admin=student_id["student_id"])
                        status = True if student_id["attendance_status"] == 1 else False
                    
                        attendence_report = AttendenceReport(student_id = student,attendence_id = attendence,status=status)
                        attendence_report.save()
                    
                        print(f"Attendance saved for student ID: {student_id["student_id"]}")
            
                        
                print("Attendance saved successfully")

            messages.success(request, "Attendance submitted successfully!")
            return JsonResponse({"success": 200})

        except Exception as e:
            print(f"Failed to save attendance: {e}")
            messages.error(request, "Error! Failed to submit attendance.")
            return JsonResponse({"FAILED": 400})
        


def staff_update_attendence(request):
    staff = Staff.objects.get(admin =request.user)
    subjects = Subject.objects.filter(staff_id = staff.id)
    session_years = SessionYear.objects.all()
    return render(request,"staff_template/staff_update_attendence.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_attendence_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")

    subject_obj = Subject.objects.get(id = subject)
    session_year_obj = SessionYear.objects.get(id = session_year_id)
    attendence = Attendence.objects.filter(subject_id = subject,session_year_id= session_year_obj)
    attendence_obj = []
    for attendence_i in attendence:
        data = {"id":attendence_i.id , "date":str(attendence_i.attendence_date),"session_year":attendence_i.session_year_id.id}
        attendence_obj.append(data)

    return JsonResponse(json.dumps(attendence_obj),content_type ="application/json",safe=False)


@csrf_exempt
def get_attendence_students(request):
    if request.method == "POST":
        attendence_id = request.POST.get("attendence_date")
        try:
            attendence_id = int(attendence_id)
        except ValueError:
            return JsonResponse({"error": "Invalid Subject or Session Year ID"}, status=400)

      
        try:
            attendence_obj = Attendence.objects.get(id=attendence_id)
        except SessionYear.DoesNotExist:
            return JsonResponse({"error": "Attendence date not found"}, status=404)

        # Query students
        attendence_data = AttendenceReport.objects.filter(
            attendence_id = attendence_obj
        )

        list_data = []
        for attendence_i in attendence_data:
            data_small = {"id":attendence_i.id,"student_id":attendence_i.student_id.admin.id,"student_name" :f"{attendence_i.student_id.admin.first_name} {attendence_i.student_id.admin.last_name}" ,"status":attendence_i.status}
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type ="application/json",safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # Use csrf_exempt only during development; use CSRF tokens in production
def update_attendance_data(request):
    if request.method == "POST":
        
            # Parse data from the request
            attendance_date = request.POST.get("attendence_date")
            student_ids = json.loads(request.POST.get("student_ids", "[]"))
            subject_id = request.POST.get("subject_id")
            session_year_id = request.POST.get("session_year_id")

            # Validate required fields
            if not attendance_date or not subject_id or not session_year_id:
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # Fetch related Subject and SessionYear objects
            subject = Subject.objects.get(id=subject_id)
            session_year = SessionYear.objects.get(id=session_year_id)

            # Create or retrieve the attendance record for the given date, subject, and session
            subject_id = int(subject_id)
            session_id = int(session_year_id)
            attendance_date = int(attendance_date)
            attendance= Attendence.objects.get(id=attendance_date
            )

            # Process each student's attendance
            for student_id in student_ids:
                # Fetch the student object
                student_instance = Student.objects.get(admin=student_id["student_id"])
                attendance_status = True if student_id["attendance_status"] == 1 else False


                # Create or update the attendance report for the student
                AttendenceReport.objects.update_or_create(
                    student_id=student_instance,
                    attendence_id=attendance,
                    defaults={"status": bool(attendance_status)},
                )

            return JsonResponse({"message": "Attendance updated successfully!"}, status=200)

        # except Exception as e:
        #     return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)