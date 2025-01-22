from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

# Create your models here.

class CustomUser(AbstractUser):
    
    USER_TYPES = (("HOD","HOD"),("STAFF","Staff"),("STUDENT","Student"))
    user_type = models.CharField(choices=USER_TYPES,default="HOD",max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()
    # object field in all model so they return current object data

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    # name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()

    def __str__(self):
        return f"{self.admin.first_name } {self.admin.last_name}"

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()

    def __str__(self):
        return self.course_name



class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()

    def __str__(self):
        return f"{self.subject_name} : {self.course_id.course_name}"
    
class SessionYear(models.Model):
    id = models.AutoField(primary_key=True)
    academic_start_year = models.DateField()
    academic_end_year = models.DateField()
    objects=models.Manager()


    def __str__(self):
        return f"{self.academic_start_year} - { self.academic_end_year}"

   

class Student(models.Model):
    GENDER = (("FEMALE","Female"),("MALE","Male"),("OTHERS","Others"))
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    # normalizing the models
    gender = models.CharField(max_length=255 ,choices=GENDER)

    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYear,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()


class Attendence(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    attendence_date = models.DateField(auto_now_add=True)
    session_year_id = models.ForeignKey(SessionYear,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()


class AttendenceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendence_id = models.ForeignKey(Attendence,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()



class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()



class FeedbackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()

class FeedbackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()

class NotificationStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects=models.Manager()



# signaling
    # USER_TYPES = (("HOD","HOD"),("STAFF","Staff"),("STUDENT","Student"))

@receiver(post_save,sender =CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == "HOD":
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == "STAFF":
            Staff.objects.create(admin=instance,address="")
        if instance.user_type == "STUDENT":
            Student.objects.create(admin=instance,course_id=Course.objects.get(id=1),session_year_id = SessionYear.objects.get(id=1))

@receiver(post_save,sender =CustomUser)
def save_user_profile(sender,instance,**kwargs):
        if instance.user_type == "HOD":
            instance.adminhod.save()
        if instance.user_type == "STAFF":
            instance.staff.save()
        if instance.user_type == "STUDENT":
            instance.student.save()

