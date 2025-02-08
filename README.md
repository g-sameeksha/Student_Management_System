# 📚 Python Django Student Management System

A **Django & MySQL**-based system to manage students, staff, courses, attendance, and results.

## 🔖  Features
- ✅ **Role-Based Authentication** (Admin, HOD, Staff, Students)
- ✅ **Manage Students, Staff, Courses & Subjects**
- ✅ **Attendance Tracking & Leave Management**
- ✅ **Result and Feedback System**
- ✅ **Google reCAPTCHA for Security**
- ✅ **Email via SMTP for password Resetting**
- ✅ **MySQL Database Integration**

## 💡 Tech Stack
- **Backend**: Django (Python)  
- **Database**: MySQL  
- **Frontend**: HTML, CSS, JavaScript  
- **Security**: Google reCAPTCHA  
- **Email**: SMTP

---

## 🔧 Setup Instructions

### 1️⃣ Install Dependencies & Setup Virtual Environment

```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
```

#### Create & Activate Virtual Environment
```python
python -m venv venv
source venv/bin/activate
```  

#### Install Required Packages
```python
pip install -r requirements.txt
```

### 2️⃣ Configure MySQL Connection  
Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',  # or your MySQL server address
        'PORT': '3306',
    }
}
```

Run migrations:

```python
python manage.py migrate
```


### 3️⃣ Setup Google reCAPTCHA  
1. Register at [Google reCAPTCHA](https://www.google.com/recaptcha/) and get **SITE_KEY** & **SECRET_KEY**.  
2. Add the keys to `settings.py`:

```python
RECAPTCHA_PUBLIC_KEY = "your_site_key"
RECAPTCHA_PRIVATE_KEY = "your_secret_key"
```

### 4️⃣ Configure Email Sending (SMTP)

```python
Update settings.py:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password
```

### 5️⃣ Run the Server

```python
python manage.py runserver
🔗 Open http://127.0.0.1:8000/ in your browser
```
