from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename = view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "HOD":
                if modulename == "studentapp.HODviews":
                    pass
                elif modulename == "studentapp.views" or modulename =="django.views.static":
                    pass
                else:
                        return redirect("admin_home")
            if user.user_type == "Staff":
                if modulename == "studentapp.StaffViews":
                    pass
                elif modulename == "studentapp.views"or modulename =="django.views.static" :
                    pass
                else:
                        return redirect("staff_home")
            if user.user_type == "Student":
                if modulename == "studentapp.StudentViews":
                    pass
                elif modulename == "studentapp.views" or modulename =="django.views.static" :
                    pass
                else:
                        return redirect("student_home")
        else:
             if request.path == reverse("login_user") or modulename == 'django.contrib.auth.views' or modulename == 'studentapp.views':
                  pass
             else:
                  return redirect("login_user")
             


