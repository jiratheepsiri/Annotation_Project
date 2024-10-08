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
import uuid
import os
from django.core.exceptions import ValidationError



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
    if request.user.is_authenticated:
        if request.method == 'POST':
            proposed_text = request.POST.get('user_proposed_text', '').strip()  # Get input and strip whitespace
            word_class_str = request.POST.get('word_class', '0')  # Default to '0'
            word_status = request.POST.get('word_status','รออนุมัติ')
            # Validate word_class input
            word_class = int(word_class_str) if word_class_str.isdigit() else 0  # Safely convert to int

            if not proposed_text:  # Check if proposed_text is empty
                # You can add an error message or handle it as needed
                error_message = "กรุณากรอกคำที่คุณคิดว่าเป็นการบูลลี่ทางไซเบอร์"  # Example message in Thai
                return render(request, 'accounts/texttopost.html', {
                    'username': request.user.username,
                    'error_message': error_message,
                })

            text_id = generate_text_id()  # Generate the unique text_id

            bully_text = ProposedText(
                user=request.user,
                text_id=text_id,
                proposed_text=proposed_text,
                word_class=word_class,
                word_status=word_status,
                proposed_t_admin_id=None,  # Allowing NULL value
            )

            try:
                bully_text.save()  # Attempt to save the proposed text
                return redirect('texttopost')
            except Exception as e:
                # Log the exception or handle it as needed
                error_message = f"An error occurred while saving: {str(e)}"
                return render(request, 'accounts/texttopost.html', {
                    'username': request.user.username,
                    'error_message': error_message,
                })

        return render(request, 'accounts/texttopost.html', {
            'username': request.user.username,
        })
    else:
        return redirect('login')

def texttopostFile(request):
    if request.user.is_authenticated:
        print(f"Authenticated user: {request.user.username}")  # Debugging line

        if request.method == 'POST':
            uploaded_file = request.FILES.get('file')  # Get the uploaded file
            
            if uploaded_file:
                # Get the file extension
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                
                # Check if the file extension is either .csv or .xml
                if file_extension not in ['.csv', '.xml']:
                    error_message = "ไฟล์ที่อัปโหลดต้องเป็น .csv หรือ .xml เท่านั้น"  # Error message in Thai
                    return render(request, 'accounts/texttopostFile.html', {
                        'username': request.user.username,
                        'error_message': error_message,
                    })

                # Process the file (e.g., save it, read contents, etc.)
                # Your file processing logic here
                
                # Optionally, redirect to a success page
                return redirect('success_page')  # Change this to your success URL or view

            else:
                error_message = "โปรดเลือกไฟล์เพื่ออัปโหลด"  # Error message for no file selected
                return render(request, 'accounts/texttopostFile.html', {
                    'username': request.user.username,
                    'error_message': error_message,
                })

        return render(request, 'accounts/texttopostFile.html', {
            'username': request.user.username,
        })

    else:
        return redirect('login')  # Redirect to login page if not authenticated
    
    
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

def generate_text_id():
    count = ProposedText.objects.count() + 1  # Start counting from 1
    text_id = f"201{count:07d}"  # Generate ID in the format 2010000001, etc.
    return text_id

