from django.urls import include, path

from . import views,HODviews,StaffViews,StudentViews


urlpatterns = [
   # path("",views.home, name="home"),

   path("signup_admin",views.signup_admin,name="signup_admin"),
   path("signup_staff",views.signup_staff,name="signup_staff"),
   path("signup_student",views.signup_student,name="signup_student"),

   path("admin_home",HODviews.admin_home,name="admin_home"),
   path("admin_profile",HODviews.admin_profile,name="admin_profile"),
 
   path('accounts/',include('django.contrib.auth.urls')),
   path("add_session",HODviews.add_session,name="add_session"),
   path('check_email/', views.check_email_availability, name='check_email'),
   path('check_username/', views.check_username, name='check_username'),

   path("",views.login_user,name="login_user"),
   path("logout",views.logout_user,name="logout_user"),
   path("add_staff",HODviews.add_staff,name="add_staff"),
   path("manage_staff",HODviews.manage_staff,name="manage_staff"),
   path("add_course",HODviews.add_course,name="add_course"),
   path("manage_course",HODviews.manage_course,name="manage_course"),
   path("add_student",HODviews.add_student,name="add_student"),
  

   path("manage_student",HODviews.manage_student,name="manage_student"),
   path("edit_user/<int:id>/<str:user_type>",HODviews.edit_user,name="edit_user"),
   path("add_subject",HODviews.add_subject,name="add_subject"),
   path("manage_subject",HODviews.manage_subject,name="manage_subject"),
   path("edit_subject/<int:id>",HODviews.edit_subject,name="edit_subject"),
   path("edit_course/<int:id>",HODviews.edit_course,name="edit_course"),

   path('reply_feedback/<int:feedback_id>/<str:feedback_type>/', HODviews.reply_feedback, name='reply_feedback'),
   path('feedback_list/<str:feedback_type>/', HODviews.feedback_list, name='feedback_list'),
   path('leave_report/<str:user_type>/', HODviews.leave_reports, name='leave_reports'),
   path("admin_view_attendence",HODviews.admin_view_attendence,name="admin_view_attendence"),
   
   path("admin_get_attendence_dates",HODviews.admin_get_attendence_dates,name="admin_get_attendence_dates"),
   path("admin_get_attendence_students",HODviews.admin_get_attendence_students,name="admin_get_attendence_students"),


   # staff url paths

   path("staff_home",StaffViews.staff_home,name="staff_home"),
   path("staff_profile",StaffViews.staff_profile,name="staff_profile"),

   path("staff_take_attendence",StaffViews.staff_take_attendence,name="staff_take_attendence"),
   path("get_students",StaffViews.get_students,name="get_students"),
   path("save_attendance_data",StaffViews.save_attendance_data,name="save_attendance_data"),
   path("staff_update_attendence",StaffViews.staff_update_attendence,name="staff_update_attendence"),
   path("get_attendence_dates",StaffViews.get_attendence_dates,name="get_attendence_dates"),
   path("get_attendence_students",StaffViews.get_attendence_students,name="get_attendence_students"),
   path("update_attendance_data",StaffViews.update_attendance_data,name="update_attendance_data"),
   path("staff_apply_leave",StaffViews.staff_apply_leave,name="staff_apply_leave"),
   path("staff_feedback",StaffViews.staff_feedback,name="staff_feedback"),
   path("staff_add_result",StaffViews.staff_add_result,name="staff_add_result"),
   path("staff_save_marks",StaffViews.staff_save_marks,name="staff_save_marks"),
   path("staff_edit_result",StaffViews.staff_edit_result,name="staff_edit_result"),
   path("get_student_result",StaffViews.get_student_result,name="get_student_result"),
   path("update_student_result",StaffViews.update_student_result,name="update_student_result"),


   # student url paths

   path("student_home",StudentViews.student_home,name="student_home"),
   path("student_profile",StudentViews.student_profile,name="student_profile"),

   path("student_view_attendence",StudentViews.student_view_attendence,name="student_view_attendence"),
   path("student_apply_leave",StudentViews.student_apply_leave,name="student_apply_leave"),
   path("student_feedback",StudentViews.student_feedback,name="student_feedback"),
   path("student_view_result",StudentViews.student_view_result,name="student_view_result"),



]

