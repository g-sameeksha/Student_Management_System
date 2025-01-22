from django.urls import include, path

from . import views,HODviews,StaffViews,StudentViews


urlpatterns = [
   path("",views.home, name="home"),
   path("admin_home",HODviews.admin_home,name="admin_home"),

   path("manage_session",HODviews.manage_session,name="manage_session"),
   path("add_session",HODviews.add_session,name="add_session"),

   path("login",views.login_user,name="login_user"),
   path("logout",views.logout_user,name="logout_user"),
   path("add_staff",HODviews.add_staff,name="add_staff"),
   path("manage_staff",HODviews.manage_staff,name="manage_staff"),
   path("add_course",HODviews.add_course,name="add_course"),
   path("manage_course",HODviews.manage_course,name="manage_course"),
   path("add_student",HODviews.add_student,name="add_student"),
   path("manage_student",HODviews.manage_student,name="manage_student"),
   path("edit_user/<int:id>/<str:user_type>",HODviews.edit_user,name="edit_user"),
   path("student_home",StudentViews.student_home,name="student_home"),
   path("staff_home",StaffViews.staff_home,name="staff_home"),
   path("add_subject",HODviews.add_subject,name="add_subject"),
   path("manage_subject",HODviews.manage_subject,name="manage_subject"),
   path("student_home",StudentViews.student_home,name="student_home"),
   path("staff_home",StaffViews.staff_home,name="staff_home"),
   path("edit_subject/<int:id>",HODviews.edit_subject,name="edit_subject"),
   path("edit_course/<int:id>",HODviews.edit_course,name="edit_course"),

   # staff url paths

   path("staff_home",StaffViews.staff_home,name="staff_home"),
   path("staff_take_attendence",StaffViews.staff_take_attendence,name="staff_take_attendence"),
   path("get_students",StaffViews.get_students,name="get_students"),
   path("save_attendance_data",StaffViews.save_attendance_data,name="save_attendance_data"),
   # path("staff_view_attendence",StaffViews.staff_view_attendence,name="staff_view_attendence"),
   path("staff_update_attendence",StaffViews.staff_update_attendence,name="staff_update_attendence"),
   path("get_attendence_dates",StaffViews.get_attendence_dates,name="get_attendence_dates"),
   path("get_attendence_students",StaffViews.get_attendence_students,name="get_attendence_students"),
   path("update_attendance_data",StaffViews.update_attendance_data,name="update_attendance_data"),



   


   







]

