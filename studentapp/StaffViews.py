from django.shortcuts import render,redirect
from .forms import StaffForm,CourseForm,StudentForm
from django.contrib import messages
from .models import Staff,Course


def staff_home(request):
    return render(request,"staff_template/staff_home.html")

