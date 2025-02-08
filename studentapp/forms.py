from django import forms
from django.contrib.auth import get_user_model
from .models import Staff, CustomUser,Course,Student,Subject
from django.forms.widgets import DateInput


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email',
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password...',
        }),
        label="Password",
    )
    user_type = forms.ChoiceField(
        choices=[('HOD', 'Head of Department'), ('Staff', 'Staff'), ('Student', 'Student')],
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label="User Type",
    )



User = get_user_model()

class StaffForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True,widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'id': 'check_email'
        }))
    
    username = forms.CharField(max_length=255, required=True , widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'check_username',
        }))
    
    first_name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'class': 'form-control', }))
    last_name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password' }))

    class Meta:
        model = Staff
        fields = ['address']  # Include only the fields specific to the Staff model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing an existing Staff instance, prepopulate the CustomUser fields
        if self.instance.pk:
            self.fields['email'].initial = self.instance.admin.email
            self.fields['username'].initial = self.instance.admin.username
            self.fields['first_name'].initial = self.instance.admin.first_name
            self.fields['last_name'].initial = self.instance.admin.last_name

    def save(self, commit=True):
        staff_instance = super().save(commit=False)

        # Handle admin (CustomUser) creation or update
        if not staff_instance.admin:
            # Create a new CustomUser instance for the Staff
            staff_instance.admin = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type = "Staff"

            )
        else:
            # Update the existing CustomUser instance
            staff_instance.admin.email = self.cleaned_data['email']
            staff_instance.admin.username = self.cleaned_data['username']
            staff_instance.admin.first_name = self.cleaned_data['first_name']
            staff_instance.admin.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                staff_instance.admin.set_password(self.cleaned_data['password'])
            staff_instance.admin.save()

        if commit:
            staff_instance.save()

        return staff_instance


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_name"]  # Corrected capitalization of "fields"
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Name'
            })
        }
        labels = {
            'course_name': 'Course Name'
        }

class StudentForm(forms.ModelForm):
    # Fields for the CustomUser model (admin)
    username = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'check_username',
        }))
    email = forms.EmailField(max_length=255, required=True,widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'id': 'check_email'
        }))
 
    first_name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'class': 'form-control', }))
    last_name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password' }))
   

    class Meta:
        model = Student
        fields = ['gender', 'profile_pic', 'address', 'course_id',"session_year_id"]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'course_id': forms.Select(attrs={'class': 'form-select'}),
            'session_year_id': forms.Select(attrs={'class': 'form-select'}),  

        }

    def save(self, commit=True):
        # Create a CustomUser instance
       
        admin_user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type = "Student"
        )

        # Create the Student instance and associate it with the admin_user
        student = super().save(commit=False)
        student.admin = admin_user

        if commit:
            student.save()
        return student



class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields =["subject_name","course_id","staff_id"]
