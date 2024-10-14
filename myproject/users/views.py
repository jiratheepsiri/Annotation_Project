from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login
from django.db import connection
from django.contrib.auth import login as auth_login
from django.contrib import messages
from io import TextIOWrapper
from .models import user_map, Users, ProposedText, ProposedFile
import bcrypt  # Import bcrypt for password hashing
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import pytz
import uuid
import os
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import csv
import xml.etree.ElementTree as ET
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user
from django.db import models



def index(request):
    return render(request, 'index.html')  # แสดงหน้า home.html

def edit_profile(request):
    if request.user.is_authenticated:  # This works if you add is_authenticated property in Users model
        print(f"Authenticated user: {request.user.username}")  # Debugging line
        return render(request, 'accounts/edit_profile.html', {
            'username': request.user.username,
        })
    else:
        return redirect('login')  # Redirect to login page if not authenticated


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
@login_required
def texttopostFile(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            user = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
            
            file_name = uploaded_file.name
            file_type = uploaded_file.content_type.split('/')[-1]  
            file_size = float(uploaded_file.size)  
            uploaded_id = generate_upload_id()
            
            try:
                # Create ProposedFile instance first
                proposed_file = ProposedFile.objects.create(
                    upload_id=uploaded_id,
                    file_name=file_name,
                    file_type=file_type,
                    user=user,
                    file_size=file_size,
                    file_data=uploaded_file.read(),
                    uploaded_date=now(),
                    file_path=uploaded_file.name
                )

                uploaded_file.seek(0)  # Go back to the beginning of the file
                csv_reader = csv.reader(uploaded_file.read().decode('utf-8').splitlines())
                next(csv_reader)  # Skip the header

                existing_ids = ProposedText.objects.values_list('text_id', flat=True)
                existing_ids = set(str(text_id) for text_id in existing_ids)

                max_count = max((int(text_id[3:]) for text_id in existing_ids if text_id.startswith("201")), default=0)
                print(f"existing id{existing_ids}")
                for row in csv_reader:
                    existing_ids = ProposedText.objects.values_list('text_id', flat=True)
                    print(f"existing id{existing_ids}")
                    existing_ids = set(str(text_id) for text_id in existing_ids)
                    print(f"existing id{existing_ids}")
                    max_count = max((int(text_id[3:]) for text_id in existing_ids if text_id.startswith("201")), default=0)
                    print(f"max_count{max_count}")
                    if len(row) < 3:  # Check if row has enough columns
                        continue

                    word = row[0]  
                    word_class_value = row[1].strip()
                    if not word_class_value:  
                        print(f"Invalid word_class value: empty - skipping this row: {row}")
                        continue
                    
                    try:
                        word_class = int(word_class_value)  
                    except ValueError:
                        print(f"Invalid word_class value: {word_class_value} - skipping this row: {row}")
                        continue

                    word_class_type = row[2]  

                    max_count += 1
                    text_id = f"201{max_count:07d}"

                    # Ensure the generated text_id is unique
                    while text_id in existing_ids:
                        max_count += 1
                        text_id = f"201{max_count:07d}"

                    # Check for duplicate ProposedText before creating
                    if ProposedText.objects.filter(upload_id=proposed_file, text_id=text_id).exists():
                        print(f"Entry with upload_id {proposed_file.upload_id} and text_id {text_id} already exists.")
                        continue  

                    proposed_text = ProposedText.objects.create(
                        user=user,
                        proposed_text=word,
                        word_class=word_class,
                        word_status="รออนุมัติ",
                        word_class_type=word_class_type,
                        text_id=text_id,
                        upload_id=proposed_file  
                    )
                
                return redirect("texttopostFile")
                
            except Exception as e:
                print(f"Error while creating ProposedText or ProposedFile: {e}")

        return render(request, 'accounts/texttopostFile.html', {
            'username': request.user.username,
        })

    return render(request, 'accounts/texttopostFile.html', {
        'username': request.user.username,
    })




    
    
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

def generate_upload_id() -> str:
    # Get the current year
    current_year = now().year
    year_prefix = str(current_year)[-4:]  # Get the last four digits of the year
    
    # Get the last upload number for the current year
    last_upload = ProposedFile.objects.filter(upload_id__startswith=year_prefix).order_by('-upload_id').first()
    
    if last_upload:
        # Extract the last five digits and increment
        last_number = int(last_upload.upload_id[-5:]) + 1
    else:
        last_number = 1  # Start from 1 if no uploads found
    
    # Format the new upload ID, ensuring it has 5 digits
    upload_id = f"{year_prefix}{last_number:05d}"  # Pad with zeros to ensure 5 digits
    
    # Optional: Add a limit to the last_number to prevent overflow
    if last_number > 99999:
        raise ValueError("Exceeded maximum upload ID limit for the year.")
        
    return upload_id

