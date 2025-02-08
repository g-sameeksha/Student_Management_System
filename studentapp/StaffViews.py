from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm
from django.contrib import messages
from .models import CustomUser, Staff,Course,SessionYear,Subject,Student,AdminHOD,Attendence,AttendenceReport,LeaveReportStaff,FeedbackStaff,StudentResult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.contrib.sessions import serializers
from django.core import serializers
import json
from django.db import transaction
from django.http import HttpResponseRedirect ,HttpResponse



def staff_home(request):
    staff_id_curr = Staff.objects.get(admin =request.user.id)
    subjects = Subject.objects.filter(staff_id = staff_id_curr)
    subject_count = subjects.count()

    course_id_list = []
    for subject in subjects:
        course = Course.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    final_course_list = set(course_id_list)
    students_count = Student.objects.filter(course_id__in = final_course_list).count()
    print(students_count)
  

    leave_count = LeaveReportStaff.objects.filter(staff_id = staff_id_curr,leave_status =1).count()
    attendence_taken_count = Attendence.objects.filter(subject_id__in = subjects).count()

    subject_list  = []
    attendence_list = []
    for subject in subjects:
        subject_list.append(subject.subject_name)
        attendence_count = Attendence.objects.filter(subject_id = subject.id).count()
        attendence_list.append(attendence_count)


    print(subject_list)
    print(attendence_list)


    student_attendence = Student.objects.filter(course_id__in = final_course_list)

    student_list =[]
    student_list_attendence_present = []
    student_list_attendence_absent = []

    for student in student_attendence:
        attendence_present_count = AttendenceReport.objects.filter(status =True,student_id= student.id).count()
        attendence_absent_count = AttendenceReport.objects.filter(status =False,student_id = student.id).count()
        student_list_attendence_present.append(attendence_present_count)
        student_list_attendence_absent.append(attendence_absent_count)
        student_list.append(student.admin.username)




    return render(request,"staff_template/staff_home.html",
                  {"subject_count":subject_count ,"leave_count":leave_count,"students_count" :students_count,"attendence_taken_count":attendence_taken_count,"subject_list":subject_list,"attendence_list":attendence_list,"student_list":student_list,"student_list_attendence_absent":student_list_attendence_absent,"student_list_attendence_present":student_list_attendence_present})

def staff_profile(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    staff_obj = Staff.objects.get(admin= custom_user.id)
    print(custom_user.first_name)
   
    if request.method  == "POST":
        first_name_inp = request.POST.get("first_name")
        address_inp = request.POST.get("address")
        last_name_inp = request.POST.get("last_name")

        try:
            custom_user.first_name = first_name_inp
            custom_user.last_name= last_name_inp
            custom_user.save()
            staff_obj = Staff.objects.get(admin= custom_user.id)
            staff_obj.address = address_inp
            staff_obj.save()
            messages.success(request, 'Profile data updated successfully!')
            return redirect("staff_profile")
        except Exception as e:
            messages.error(request, f'Failed to update Profile')
            return redirect("staff_profile")

    return render(request,"staff_template/staff_profile.html",{"user":custom_user,"staff":staff_obj})


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



def staff_apply_leave(request):
    if request.method == "POST":
        leave_date_inp = request.POST.get("leave_date")
        leave_msg_inp = request.POST.get("leave_reason")

        staff_obj = Staff.objects.get(admin = request.user.id)
        try :
            leave_obj = LeaveReportStaff(
            staff_id = staff_obj,
            leave_date = leave_date_inp,
            leave_message = leave_msg_inp,
            leave_status =0
        )
            leave_obj.save()
            messages.success(request,"succeessfully applied for leave.Admin need to approve")
            return redirect('staff_apply_leave')
        except Exception as e:
            messages.error(request,"failed to apply for leave")
            return redirect('staff_apply_leave')
    
    staff_obj = Staff.objects.get(admin = request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id = staff_obj)

            
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})

def staff_feedback(request):
    if request.method == "POST":
        feedback_inp = request.POST.get("feedback_msg")

        staff_obj = Staff.objects.get(admin = request.user.id)
        try :
            feedback_obj = FeedbackStaff(
            staff_id = staff_obj,
            feedback = feedback_inp,
            feedback_reply = ""
        )
            feedback_obj.save()
            messages.success(request,"succeessfully submitted your feedback")
            return redirect('staff_feedback')
        except Exception as e:
            messages.error(request,"failed to submit your feedback")
            return redirect('staff_feedback')
    
    staff_obj = Staff.objects.get(admin = request.user.id)
    feedback_data = FeedbackStaff.objects.filter(staff_id = staff_obj)

    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_add_result(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id = staff_id)
    session_years = SessionYear.objects.all()
    return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})

def staff_save_marks(request):
    if request.method == "POST":
        student_id= request.POST.get("student_id")
        exam_marks = request.POST.get("exam_marks")
        assignment_marks = request.POST.get("assignment_marks")
        subject_id = request.POST.get("subject_id")

        try:
            student_obj = Student.objects.get(admin=student_id)
            subject_obj = Subject.objects.get(id=subject_id)

            newStudentResult, created = StudentResult.objects.update_or_create(
                student_id=student_obj,
                subject_id=subject_obj,
                defaults={
                    "exam_marks": exam_marks,
                    "assignment_marks": assignment_marks
                }
            )
            return JsonResponse({ "status": "success",
                "message": "Marks submitted successfully.",})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error saving marks: {str(e)}"}, status=500)


        
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id = staff_id)
    session_years = SessionYear.objects.all()
    return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})


def staff_edit_result(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id = staff_id)
    session_years = SessionYear.objects.all()
    return render(request,"staff_template/staff_edit_marks.html",{"subjects":subjects,"session_years":session_years})
    

@csrf_exempt
def get_student_result(request):
    student_id = request.POST.get("student_id")
    subject_id = request.POST.get("subject")
    student_obj = Student.objects.get(admin=student_id)

    try:
        result = StudentResult.objects.get(student_id=student_obj, subject_id=subject_id)
        return JsonResponse({
            "exam_marks": result.exam_marks,
            "assignment_marks": result.assignment_marks
        })
    except StudentResult.DoesNotExist:
        return JsonResponse({"exam_marks": "", "assignment_marks": ""})

@csrf_exempt  
def update_student_result(request):
    student_id = request.POST.get("student_id")
    subject_id = request.POST.get("subject")
    exam_marks = request.POST.get("exam_marks")
    assignment_marks = request.POST.get("assignment_marks")

    student_obj = Student.objects.get(admin=student_id)
    subject_obj = Subject.objects.get(id=subject_id)


    try:
        result, created = StudentResult.objects.update_or_create(
            student_id=student_obj,
            subject_id=subject_obj,
            defaults={"exam_marks": exam_marks, "assignment_marks": assignment_marks}
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
