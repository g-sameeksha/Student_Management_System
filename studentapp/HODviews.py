from django.shortcuts import render,redirect,get_object_or_404
from .forms import StaffForm,CourseForm,StudentForm,SubjectForm
from django.contrib import messages
from .models import Staff,Course,Subject,Student,CustomUser,SessionYear,FeedbackStaff,FeedbackStudent,LeaveReportStaff,LeaveReportStudent,Attendence,AttendenceReport
from django.http import HttpResponseRedirect ,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def admin_home(request):
    students = Student.objects.all()
    students_count = students.count()
    
    courses = Course.objects.all()
    courses_count = courses.count()

    subjects= Subject.objects.all()
    subjects_count = subjects.count()

    staffs = Staff.objects.all()
    staffs_count = staffs.count()

    subject_count_per_course= []
    student_count_per_course = []
    course_names = []
    for course in courses:
        course_names.append(course.course_name)
        # count =0
        # for subject in subjects:
        #     if course.id == subject.course_id.id:
        #         count+=1
        subject_count  = Subject.objects.filter(course_id = course.id).count()
        student_count = Student.objects.filter(course_id = course.id).count() 
        subject_count_per_course.append(subject_count)
        student_count_per_course.append(student_count)

    student_count_per_subject = []
    subject_names = []
    for subject in subjects:
        course = Course.objects.get(id = subject.course_id.id)
        student_count = Student.objects.filter(course_id = course).count()
        subject_names.append(subject.subject_name)
        student_count_per_subject.append(student_count)
    

    attendence_absent_list_staff =[]
    attendence_present_list_staff =[]
    staff_names =[]
    for staff in staffs:
        subject_ids = Subject.objects.filter(staff_id = staff.id)
        attendence = Attendence.objects.filter(subject_id__in = subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id = staff.id,leave_status =1).count()
        staff_names.append(staff.admin.username)
        attendence_present_list_staff.append(attendence)
        attendence_absent_list_staff.append(leaves)

    attendence_absent_list_student = []
    attendence_present_list_student = []
    student_names  =[]
    for student in students:
        attendence_present = AttendenceReport.objects.filter(student_id = student.id,status =True).count()
        attendence_absent = AttendenceReport.objects.filter(student_id = student.id,status =False).count()
        leaves = LeaveReportStudent.objects.filter(student_id = student.id,leave_status =1).count()
        attendence_absent_list_student.append(attendence_absent+leaves)
        attendence_present_list_student.append(attendence_present)
        student_names.append(student.admin.username)


    return render(request,"hod_template/admin_home.html",
                  {
                      "students_count":students_count ,"staffs_count":staffs_count,"courses_count":courses_count,"subjects_count":subjects_count,
                      "subject_count_per_course":subject_count_per_course,"course_names":course_names,"student_count_per_course":student_count_per_course,
                      "student_count_per_subject":student_count_per_subject ,"subject_names":subject_names,
                      "staff_names" : staff_names,"attendence_present_list_staff":attendence_present_list_staff,"attendence_absent_list_staff":attendence_absent_list_staff,
                      "student_names":student_names,"attendence_absent_list_student":attendence_absent_list_student,"attendence_present_list_student":attendence_present_list_student
                  })


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    print(user.first_name)
   
    if request.method  == "POST":
        first_name_inp = request.POST.get("first_name")
        last_name_inp = request.POST.get("last_name")

        if not first_name_inp or not last_name_inp:
            messages.info(request," one or more input fields are empty")
            return redirect("admin_profile")
        
        if first_name_inp ==  request.user.first_name or last_name_inp == request.user.last_name:
            messages.info(request,"No changes to update")
            return redirect("admin_profile")


        try:
            user.first_name = first_name_inp
            user.last_name= last_name_inp
            user.save()
            messages.success(request, 'Profile data updated successfully!')
            return redirect("admin_profile")
        except Exception as e:
            messages.error(request, f'Failed to update Profile')
            return redirect("admin_profile")

    return render(request,"hod_template/admin_profile.html",{"user":user})


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request,"Staff added successfully")
                return redirect('add_staff') 
            else:
                messages.error(request, 'Error adding staff member. Please check the form.')
                return redirect("add_staff")
        except:
            messages.error(request, 'Error adding staff member. Please check the form.')
            return redirect("add_staff")
    else:
        form = StaffForm()

    return render(request, 'hod_template/add_staff.html', {'form': form})

def manage_staff(request):
    staffs = Staff.objects.all()
    staff_courses = {staff: Subject.objects.filter(staff_id=staff.id) for staff in staffs}
    # print(staff_courses)
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs,"subjects":staff_courses,"staff_courses":staff_courses})

def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('add_course')  # Update to your desired URL
        else:
            messages.error(request, 'Error adding a new Course. Please check the form.')
    else:
        form = CourseForm()

    return render(request, 'hod_template/add_course.html', {'form': form})



def manage_course(request):
    courses = Course.objects.all()
    print(courses)
    return render(request,"hod_template/manage_course.html",{"courses":courses})

def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'subject added successfully!')
            return redirect('add_subject')  # Update to your desired URL
        else:
            messages.error(request, 'Error adding a new Subject. Please check the form.')
    else:
        form = SubjectForm()

    return render(request, 'hod_template/add_subject.html', {'form': form})

def manage_subject(request):
    subjects = Subject.objects.all()
    # staff_subjects = {subject.subject_name:Staff.objects.filter(id == subject.staff_id.id)  for subject in subjects}
    # print(subjects[0].staff_id.id)

    # print(staff_subjects)
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})

def edit_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    print(staff.admin)
    if request.method == "POST":
        user = CustomUser.objects.get(id= staff_id)
        user.username= request.POST.get("username")
        # user.password = request.POST.get("password")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name= request.POST.get("last_name")
        user.save()
        staff.address=request.POST.get("address")
        
        staff.save()
        messages.success(request,f"{user.username} details saved successfully")
        return redirect(f"/edit_staff/{staff_id}")

    return render(request,'hod_template/edit_staff.html',{"user":staff,"student":False})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()  # Handles both CustomUser and Student creation
                messages.success(request, 'Student added successfully!')
                return redirect('add_student')
            except Exception as e:
                messages.error(request, f'Error while adding student: {e}')
        else:
            messages.error(request, 'Invalid form submission. Please check the details.')
    else:
        form = StudentForm()

    return render(request, 'hod_template/add_student.html', {'form': form})





def manage_student(request):
    students = Student.objects.all()
    print(students)
    return render(request,"hod_template/manage_student.html",{"students":students})


def edit_user(request,id,user_type):
    try:
        user = CustomUser.objects.get(id=id,user_type=user_type)
    except:
        return redirect("admin_home")
    courses = Course.objects.all()
    if user_type=="Student":
        student = Student.objects.get(admin=user)
        user_address=student.address
        user_profile_pic = student.profile_pic
        user_gender = student.gender
        user_academic_start_year = student.session_year_id.academic_start_year
        user_academic_end_year = student.session_year_id.academic_end_year
        user_course_name = student.course_id.course_name
        user_type="Student"
    elif user_type == "Staff":
        staff = Staff.objects.get(admin=user)
        user_address=staff.address
        user_type="Staff"
 
    if user_type == "Student":
         student_data ={
            "profile_pic" : user_profile_pic,
            "gender" : user_gender,
            "academic_start_year": user_academic_start_year,
            "academic_end_year": user_academic_end_year,
            "course_name":user_course_name}
    else:
        student_data =None

    if request.method =="POST":
        user.username= request.POST.get("username")
        # user.password = request.POST.get("password")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name= request.POST.get("last_name")
        user.save()
        if user_type=="Student":
            student.address=request.POST.get("address")
            profile_pic = request.FILES.get("profile_pic")
            if profile_pic:
                student.profile_pic = profile_pic
    
            student.gender=request.POST.get("gender")
            student.session_year_id.academic_start_year=request.POST.get("academic_start_year")
            student.session_year_id.academic_end_year=request.POST.get("academic_end_year")
            student.course_id = Course.objects.get(id = request.POST.get("course_id"))
            student.save()
            messages.success(request,f"{user.username} details saved successfully")
            return redirect(f"/edit_user/{id}/{user_type}")
        elif user_type == "Staff":
            staff.address=request.POST.get("address")    
            staff.save()

        messages.success(request,f"{user.username} details saved successfully")
        return redirect(f"/edit_user/{id}/{user_type}")
    return render(request,"hod_template/edit_user.html",{"user":user,"courses":courses,"user_address":user_address,"user_type":user_type,"student":student_data})


def edit_subject(request,id):
    subject = Subject.objects.get(pk=id)
    courses = Course.objects.all()
    staffs = Staff.objects.all()
    if request.method =="POST":
        subject.subject_name = request.POST.get("subject_name")
        subject.course_id = Course.objects.get(id =  request.POST.get("course_id"))
        subject.staff_id = Staff.objects.get(id= request.POST.get("staff_id"))
        subject.save()
        messages.success(request,"Subject edited successfully")
        return redirect(f"/edit_subject/{id}")

    
    return render(request,"hod_template/edit_subject.html",{"subject":subject,"courses":courses,"staffs":staffs})

def edit_course(request,id):
    course = Course.objects.get(pk=id)
 
    if request.method =="POST":
        course.course_name = request.POST.get("course_name")
        
        course.save()
        messages.success(request,"Course edited successfully")
        return redirect(f"/edit_course/{id}")

    
    return render(request,"hod_template/edit_course.html",{"course":course})
    

def add_session(request):
    if request.method == "POST":
        try:
            sessionYear = SessionYear(
                academic_start_year= request.POST.get("academic_start_year"),
                academic_end_year=request.POST.get("academic_end_year")
            )
            sessionYear.save()
            messages.success(request,"Successfully added session")
            return redirect("add_session")
        except Exception as e:
            messages.error(request,"failed to add ")
            print(e)
            return redirect("add_session")
    return render(request,"hod_template/add_session_year.html")


def reply_feedback(request, feedback_id, feedback_type):
    if feedback_type == 'student':
        feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
    elif feedback_type == 'staff':
        feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
    else:
        return redirect('feedback_list', feedback_type='student')

    if request.method == 'POST':
        reply_message = request.POST.get('reply')
        
        feedback.feedback_reply = reply_message
        feedback.save()

        if feedback_type == 'student':
            return redirect(f'/feedback_list/{feedback_type}')
        elif feedback_type == 'staff':
            return redirect(f'/feedback_list/{feedback_type}')

    return render(request, 'hod_template/reply_feedback.html', {'feedback': feedback,"feedback_type":feedback_type})


def feedback_list(request, feedback_type):
    if feedback_type == 'student':
        feedbacks = FeedbackStudent.objects.all()
    elif feedback_type == 'staff':
        feedbacks = FeedbackStaff.objects.all()
    else:
        feedbacks = None  
    return render(request, 'hod_template/feedback_list.html', {'feedbacks': feedbacks, 'feedback_type': feedback_type})



def leave_reports(request, user_type):
    if user_type == 'staff':
        leave_reports = LeaveReportStaff.objects.all()
    elif user_type == 'student':
        leave_reports = LeaveReportStudent.objects.all()
    else:
        leave_reports = []  # If invalid user_type, return an empty list or handle appropriately

    # Handle approval or rejection
    if request.method == 'POST':
        leave_report_id = request.POST.get('leave_report_id')
        action = request.POST.get('action')

        try:
            # Fetch the correct leave report based on user_type
            if user_type == 'staff':
                leave_report = LeaveReportStaff.objects.get(id=leave_report_id)
            elif user_type == 'student':
                leave_report = LeaveReportStudent.objects.get(id=leave_report_id)

            if action == 'approve':
                leave_report.leave_status = 1  # Approved
            elif action == 'reject':
                leave_report.leave_status = 2  # Rejected

            leave_report.save()

        except (LeaveReportStaff.DoesNotExist, LeaveReportStudent.DoesNotExist):
            pass

        # Redirect or re-render the page after processing
        return render(request, "hod_template/leave_reports.html", {"leave_reports": leave_reports, "user_type": user_type})

    return render(request, "hod_template/leave_reports.html", {"leave_reports": leave_reports, "user_type": user_type})




def admin_view_attendence(request):
    subjects = Subject.objects.all()
    session_years = SessionYear.objects.all()
    return render(request,"hod_template/admin_view_attendence.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def admin_get_attendence_dates(request):
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
def admin_get_attendence_students(request):
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

