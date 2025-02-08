from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm ,StaffForm,StudentForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect ,HttpResponse
from .HODviews import admin_home
import requests
import json
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


User = get_user_model() 

# Create your views here.
def home(request):
    return render(request,'home.html')





def login_user(request):
    if request.method == 'POST':
        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_server_url ="https://www.google.com/recaptcha/api/siteverify"
        captcha_secret_key = "6Lek18oqAAAAAGz2zmrn6aE-bOBb3INJNzqWMjH_"
        captcha_data = {
            "secret":captcha_secret_key,
            "response":captcha_token
        }
        captcha_server_response = requests.post(url=captcha_server_url,data=captcha_data)

        captcha_json = json.loads(captcha_server_response.text)

        if captcha_json["success"] == False:
              messages.error(request, 'Invalid Captcha .Try Again')
              return redirect("login_user")


        # print("captcha token : "+captcha_token)
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            print(email,password,user_type)

            try:
                # Retrieve the user based on email and user_type
                user = User.objects.get(email=email, user_type=user_type)
                user = authenticate(request, username=user.username, password=password)
                print(user)
                if user!=None:
                    login(request, user)
                    if user.user_type == "HOD":
                        return redirect("admin_home")
                    if user.user_type == "Student":
                        return redirect("student_home")
                    if user.user_type == "Staff":
                        return redirect("staff_home")
                else:
                    messages.error(request, "Invalid email or password!")
            except User.DoesNotExist:
                # form.add_error(None, 'No account found with the provided email and user type')
                messages.error(request, 'No account found with the provided email and user type')

    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User: "+request.user.email+"usertype: "+request.user.user_type )
    else:
        return HttpResponse("Please Login first")
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup_admin(request):
     if request.method == "POST":
         username_inp = request.POST.get("username")
         email_inp = request.POST.get("email")
         password_inp = request.POST.get("password1")
         password_confirm_inp = request.POST.get("password2")
         
         if password_inp != password_confirm_inp:
            messages.error(request,"Passwords doesn't match")
            return redirect("signup_admin")
             


         try:
            user = CustomUser.objects.create_user(username=username_inp,email=email_inp,password=password_inp,user_type='HOD')
            user.save()

            print(f"{username_inp}{email_inp}{password_inp}")
            messages.success(request,"Admin user created successfully")
            return redirect("signup_admin")
         except:
            messages.error(request, 'Failed to Create admin.')
            return redirect("signup_admin")
         
     return render(request,"signup_admin.html")

def signup_staff(request):
    if request.method == 'POST':
        if request.POST.get("password") != request.POST.get("check_password"):
            messages.error(request, 'Passwords are not matching')
            return redirect("signup_staff")

        form = StaffForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request,"Staff user created successfully")
                return redirect('signup_staff') 
            else:
                messages.error(request, 'failed to create Staff user')
                return redirect("signup_staff")
        except:
            messages.error(request, 'failed to create Staff user')
            return redirect("signup_staff")
    else:
        form = StaffForm()

    return render(request, 'signup_staff.html', {'form': form})

def signup_student(request):



    # if request.method == 'POST':
    #     form = StudentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         try:
    #             form.save()  # Handles both CustomUser and Student creation
    #             messages.success(request, 'Student added successfully!')
    #             return redirect('signup_student')
    #         except Exception as e:
    #             messages.error(request, f'Error while adding student: {e}')
    #     else:
    #         messages.error(request, 'Invalid form submission. Please check the details.')
    # else:
    #     form = StudentForm()

    # return render(request, 'signup_student.html', {'form': form})


    if request.method == 'POST':
        if request.POST.get("password") != request.POST.get("check_password"):
            messages.error(request, 'Passwords are not matching')
            return redirect("signup_student")

        form = StudentForm(request.POST, request.FILES)  
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student user created successfully")
                return redirect('signup_student')
            except Exception as e:
                print(form.errors)
                messages.error(request, f'Failed to create Student user: {e}')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form submission. Please check the details.')
    else:
        form = StudentForm()

    return render(request, 'signup_student.html', {'form': form})



@csrf_exempt
def check_email_availability(request):
    if request.method =="POST":
        email = request.POST.get('email', '')
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'available': False, 'message': 'Email is already in use.'})
        return JsonResponse({'available': True, 'message': 'Email is available.'})



@csrf_exempt
def check_username(request):
    username = request.POST.get('username','')
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({'available': False, 'message': 'Username is already in use.'})
    return JsonResponse({'available': True, 'message': 'Username is available.'})