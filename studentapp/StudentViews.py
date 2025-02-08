from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm
from django.contrib import messages
from .models import Course,LeaveReportStudent,FeedbackStudent,Student,Subject,CustomUser,Attendence,AttendenceReport,StudentResult
import datetime
from django.http import HttpResponseRedirect ,HttpResponse
from django.views.decorators.csrf import csrf_exempt


def student_home(request):
    student_obj = Student.objects.get(admin=request.user.id)
    attendence_total = AttendenceReport.objects.filter(student_id = student_obj).count()
    attendence_present = AttendenceReport.objects.filter(student_id = student_obj,status =True).count()
    attendence_absent = AttendenceReport.objects.filter(student_id = student_obj,status =False).count()
    course_id = Course.objects.get(id = student_obj.course_id.id)
    subjects = Subject.objects.filter(course_id=course_id)
    subject_count = subjects.count()
    

    subject_name =[]
    data_present = []
    data_absent = []
    for subject  in subjects:
        attendence  = Attendence.objects.filter(subject_id = subject.id)
        attendence_present_count = AttendenceReport.objects.filter(attendence_id__in = attendence,student_id = student_obj,status=True).count()
        attendence_absent_count = AttendenceReport.objects.filter(attendence_id__in = attendence,student_id = student_obj,status=False).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendence_present_count)
        data_absent.append(attendence_absent_count)

    return render(request,"student_template/student_home.html",
                  {"attendence_total":attendence_total,"attendence_present":attendence_present,"attendence_absent":attendence_absent,"subjects":subject_count,"subject_name":subject_name,"data_present":data_present,"data_absent":data_absent})

def student_profile(request):
    custom_user = CustomUser.objects.get(id=request.user.id)
    student_obj = Student.objects.get(admin= custom_user.id)

    print(custom_user.first_name)
   
    if request.method  == "POST":
        first_name_inp = request.POST.get("first_name")
        address_inp = request.POST.get("address")
        last_name_inp = request.POST.get("last_name")

        try:
            custom_user.first_name = first_name_inp
            custom_user.last_name= last_name_inp
            custom_user.save()
            student_obj = Student.objects.get(admin= custom_user.id)
            student_obj.address = address_inp
            student_obj.save()
            messages.success(request, 'Profile data updated successfully!')
            return redirect("student_profile")
        except Exception as e:
            messages.error(request, f'Failed to update Profile')
            return redirect("student_profile")

    return render(request,"student_template/student_profile.html",{"user":custom_user,"student":student_obj})


def student_view_attendence(request):
    if request.method == "POST":
        subject_inp_id = request.POST.get("subject")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if not subject_inp_id or not start_date or not end_date:
            messages.info(request,"please select all the inputs")
            return redirect("student_view_attendence")
        
        start_date_parse = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date_parse = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        subject_obj = Subject.objects.get(id=subject_inp_id)
        user_obj = CustomUser.objects.get(id=request.user.id)
        student_obj = Student.objects.get(admin = user_obj)
        attendence_data = Attendence.objects.filter(attendence_date__range = (start_date_parse,end_date_parse),subject_id=subject_obj)
        attendenceReport_data =AttendenceReport.objects.filter(attendence_id__in=attendence_data,student_id=student_obj)
        return render(request,"student_template/student_attendence_data.html",{"attendenceReport_data":attendenceReport_data})

    student = Student.objects.get(admin=request.user.id)
    course_id = student.course_id.id
    subjects = Subject.objects.filter(course_id=course_id)
    return render(request,"student_template/student_view_attendence.html",{"subjects":subjects})


def student_apply_leave(request):
    if request.method == "POST":
        leave_date_inp = request.POST.get("leave_date")
        leave_msg_inp = request.POST.get("leave_reason")
        if not leave_date_inp or not leave_msg_inp :
            messages.info(request,"please select all the inputs")
            return redirect("student_apply_leave")
        


        student_obj = Student.objects.get(admin = request.user.id)
        try :
            leave_obj = LeaveReportStudent(
            student_id = student_obj,
            leave_date = leave_date_inp,
            leave_message = leave_msg_inp,
            leave_status =0
        )
            leave_obj.save()
            messages.success(request,"succeessfully applied for leave.Admin need to approve")
            return redirect('student_apply_leave')
        except Exception as e:
            messages.error(request,"failed to apply for leave")
            return redirect('student_apply_leave')
    
    student_obj = Student.objects.get(admin = request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id = student_obj)

            
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})



def student_feedback(request):
    if request.method == "POST":
        feedback_inp = request.POST.get("feedback_msg")
        if not feedback_inp:
            messages.info(request,"enter the feedback!")
            return redirect("student_feedback")

        student_obj = Student.objects.get(admin = request.user.id)
        try :
            feedback_obj = FeedbackStudent(
            student_id = student_obj,
            feedback = feedback_inp,
            feedback_reply = ""
        )
            feedback_obj.save()
            messages.success(request,"succeessfully submitted your feedback")
            return redirect('student_feedback')
        except Exception as e:
            messages.error(request,"failed to submit your feedback")
            return redirect('student_feedback')
    
    student_obj = Student.objects.get(admin = request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id = student_obj)

    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})



def student_view_result(request):
    student = Student.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id = student)

    return render(request,"student_template/student_view_result.html",{"student_result":student_result})

