from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect ,HttpResponse
from .HODviews import admin_home

User = get_user_model() 

# Create your views here.
def home(request):
    return render(request,'home.html')





def login_user(request):
    if request.method == 'POST':
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
    return HttpResponseRedirect("/home")