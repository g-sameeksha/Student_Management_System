from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm,SubjectForm
from django.contrib import messages
from .models import Staff,Course,Subject,Student,CustomUser
from django.http import HttpResponseRedirect ,HttpResponse
from django.core.files.storage import FileSystemStorage

def admin_home(request):
    return render(request,"hod_template/base_template.html")


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')  # Update to your desired URL
        else:
            messages.error(request, 'Error adding staff member. Please check the form.')
    else:
        form = StaffForm()

    return render(request, 'hod_template/add_staff.html', {'form': form})

def manage_staff(request):
    staffs = Staff.objects.all()
    staff_courses = {staff: Subject.objects.filter(staff_id=staff.id) for staff in staffs}


    print(staff_courses)

    # 13:50 part 6
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
    user = CustomUser.objects.get(id=id,user_type=user_type)
    courses = Course.objects.all()
    if user_type=="Student":
        student = Student.objects.get(admin=user)
        user_address=student.address
        user_profile_pic = student.profile_pic
        user_gender = student.gender
        user_academic_start_year = student.academic_start_year
        user_academic_end_year = student.academic_end_year
        user_course_name = student.course_id.course_name
        user_type="Student"
    elif user_type == "Staff":
        staff = Staff.objects.get(admin=user)
        user_address=staff.address
        user_type="Staff"
      


    # print(staff?staff:"null")
    # print(student?student:"null")


    if user_type == "Student":
         student_data ={
            "profile_pic" : user_profile_pic,
            "gender" : user_gender,
            "academic_start_year": user_academic_start_year,
            "academic_end_year": user_academic_end_year,
            "course_name":user_course_name}
    else:
        student =None
    

    
    # print(student)
    if request.method =="POST":
        user.username= request.POST.get("username")
        # user.password = request.POST.get("password")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name= request.POST.get("last_name")
        user.save()
        if user_type=="Student":
            student.address=request.POST.get("address")
            profile_pic = request.FILES.get("profile_pic",False)
            fs= FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            student.profile_pic = fs.url(filename)
           

            student.gender=request.POST.get("gender")
            student.academic_start_year=request.POST.get("academic_start_year")
            student.academic_end_year=request.POST.get("academic_end_year")
            student.course_id = Course.objects.get(id = request.POST.get("course_id"))
            student.save()
        elif user_type == "Staff":
            staff.address=request.POST.get("address")    
            staff.save()


        # print(staff)
        # print(student)
        print("*****************")
        print(user)
      

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
    