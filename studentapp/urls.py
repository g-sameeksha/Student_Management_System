from django.urls import include, path

from . import views,HODviews,StaffViews,StudentViews


urlpatterns = [
   path("home",views.home, name="home"),
   path("admin_home",HODviews.admin_home,name="admin_home"),
   path("login",views.login_user,name="login_user"),
   path("logout",views.logout_user,name="logout_user"),
   path("add_staff",HODviews.add_staff,name="add_staff"),
   path("manage_staff",HODviews.manage_staff,name="manage_staff"),
   path("add_course",HODviews.add_course,name="add_course"),
   path("manage_course",HODviews.manage_course,name="manage_course"),
   path("add_student",HODviews.add_student,name="add_student"),
   # path("manage_student",HODviews.manage_staff,name="manage_staff"),
   path("student_home",StudentViews.student_home,name="student_home"),
   path("staff_home",StaffViews.staff_home,name="staff_home"),
   path("add_subject",HODviews.add_subject,name="add_subject"),
   # path("manage_student",HODviews.manage_staff,name="manage_staff"),
   path("student_home",StudentViews.student_home,name="student_home"),
   path("staff_home",StaffViews.staff_home,name="staff_home"),


]

