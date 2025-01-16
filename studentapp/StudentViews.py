from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm
from django.contrib import messages
from .models import Staff,Course


def student_home(request):
    return render(request,"hod_template/base_template.html")

