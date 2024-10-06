from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import connection
from django.contrib import messages
from .models import user_map, Users
import bcrypt  # Import bcrypt for password hashing
from django.contrib.auth.hashers import check_password


def index(request):
    return render(request, 'index.html')  # แสดงหน้า home.html

def login(request):
    msg = None

    if request.method == 'POST':
        print("POST Data:", request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}, Password: {password}")

        if username is None or password is None:
            msg = "Both fields are required."
            print(msg)
        else:
            try:
                user = Users.objects.get(username=username)
                # Check hashed password
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    # Log the user in
                    print(f"User {username} logged in successfully.")
                    return redirect('/mainlogin')
                else:
                    msg = 'Error Login: Invalid password'
                    print(msg)
            except Users.DoesNotExist:
                msg = 'Error Login: User does not exist'
                print(msg)

    return render(request, 'login.html', {'msg': msg})



def mainlogin(request):
    return render(request, 'mainlogin.html')

def annotatepage(request):
    return render(request, 'annotatepage.html')
def forgotpass(request):
    return render(request, 'forgotpass.html')
def texttopost(request):
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
            tel=tel
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
