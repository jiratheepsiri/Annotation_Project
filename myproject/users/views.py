from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.db import connection
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import user_map, Users, ProposedText
import bcrypt  # Import bcrypt for password hashing
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import pytz



def index(request):
    return render(request, 'index.html')  # แสดงหน้า home.html



def login_view(request):
    msg = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login for username: {username}")

        if not username or not password:
            msg = "Both fields are required."
            return render(request, 'login.html', {'error_message': msg})

        # Specify the backend to use
        user = authenticate(request, username=username, password=password, backend='users.backends.CustomUserBackend')

        if user is not None:
            user.last_login = timezone.now()  # Update last_login
            user.save()  # Save the user instance with the updated last_login
            login(request, user)  # Log the user in
            return redirect('accounts/mainlogin')  # Redirect to your desired page
        else:
            print("Invalid username or password.")
            msg = "Invalid username or password."

        return render(request, 'login.html', {'error_message': msg})

    return render(request, 'login.html', {'msg': msg})


def mainlogin(request):
    if request.user.is_authenticated:  # This works if you add is_authenticated property in Users model
        print(f"Authenticated user: {request.user.username}")  # Debugging line
        return render(request, 'accounts/mainlogin.html', {
            'username': request.user.username,
        })
    else:
        return redirect('login')  # Redirect to login page if not authenticated

def annotatepage(request):
    return render(request, 'annotatepage.html')

def annotateselect(request):
    return render(request, 'annotateselect.html')
def forgotpass(request):
    return render(request, 'forgotpass.html')

def texttopost(request):
    if request.method == 'POST':
        user_proposed_text = request.POST.get('user_proposed_text')
        if user_proposed_text:  # Check if the text is not empty
            # Create and save the ProposedText instance
            new_entry = ProposedText(
                proposed_t_user_id=request.user,
                user_proposed_text=user_proposed_text,
                word_status='awaiting'
            )
            return redirect('/mainlogin')  # Redirect to your success page

        # If text is empty, render the form again with an error message
        else:
            msg = "Please enter some text."
            return render(request, 'texttopost.html', {'error_message': msg})

    return render(request, 'texttopost.html')


def texttopostFile(request):
    return render(request, 'texttopostFile.html')
def txtverify(request):
    return render(request, 'txtverify.html')
def txtverifyFile(request):
    return render(request, 'txtverifyFile.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm-email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        tel = request.POST.get('telephone-number')

        # Check if the passwords match
        if password != confirm_password:
            return render(request, 'registration.html', {
                'error_message': "รหัสผ่านไม่ตรงกัน",
                'success_message': None
            })

        # Check if the emails match
        if email != confirm_email:
            return render(request, 'registration.html', {
                'error_message': "อีเมลไม่ตรงกัน",
                'success_message': None
            })

        # Check if username, email, or telephone number already exists
        if user_map.objects.filter(username=username).exists():
            return render(request, 'registration.html', {
                'error_message': "ชื่อผู้ใช้นี้มีอยู่แล้ว",
                'success_message': None
            })

        if user_map.objects.filter(email=email).exists():
            return render(request, 'registration.html', {
                'error_message': "อีเมลนี้มีอยู่แล้ว",
                'success_message': None
            })

        if user_map.objects.filter(tel=tel).exists():
            return render(request, 'registration.html', {
                'error_message': "หมายเลขโทรศัพท์นี้มีอยู่แล้ว",
                'success_message': None
            })

        user_id = generate_user_id()  # Replace with your user ID generation logic

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save the new user entry with the hashed password
        new_entry = user_map(
            user_id=user_id,
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            tel=tel,
            user_role="user"
        )
        new_entry.save()
        return render(request, 'registration.html', {
            'error_message': None,
            'success_message': "สมัครสมาชิกเรียบร้อยแล้ว"
        })

    return render(request, 'registration.html', {
        'error_message': None,
        'success_message': None
    })


def generate_user_id():
    # นับจำนวนผู้ใช้ทั้งหมดที่มีอยู่แล้ว
    count = user_map.objects.count() + 1  # ลำดับที่ 1, 2, 3, ...
    
    # สร้างเลข user_id โดยต่อเลข 164 กับลำดับที่มีความยาว 7 หลัก
    user_id = f"164{count:07d}"  # เช่น 1640000001, 1640000002
    return user_id
