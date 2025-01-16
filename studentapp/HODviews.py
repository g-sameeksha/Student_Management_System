from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm,SubjectForm
from django.contrib import messages
from .models import Staff,Course,Subject,Student,CustomUser


def admin_home(request):
    return render(request,"hod_template/base_template.html")


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member added successfully!')
            return redirect('admin_home')  # Update to your desired URL
        else:
            messages.error(request, 'Error adding staff member. Please check the form.')
    else:
        form = StaffForm()

    return render(request, 'hod_template/add_staff.html', {'form': form})

def manage_staff(request):
    staffs = Staff.objects.all()
    courses ={}
    for staff in staffs:
        courses[staff] = Subject.objects.filter(staff_id= staff.id)
    print(courses)

    print(staffs)
    # 13:50 part 6
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs,"courses":courses})

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