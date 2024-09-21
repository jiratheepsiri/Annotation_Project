from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user_map

def index(request):
    return render(request, 'index.html')  # แสดงหน้า home.html
def login(request):
    return render(request, 'login.html')  # แสดงหน้า login.html
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
    # รับค่าจาก GET request
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm-email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        tel = request.POST.get('telephone-number')
        
        if password != confirm_password:
            messages.error(request, "รหัสผ่านไม่ตรงกัน")
            return render(request, 'registration.html')
        
        if email != confirm_email:
            messages.error(request, "อีเมลไม่ตรงกัน")
            return render(request, 'registration.html')
        
        user_id = generate_user_id()

        # บันทึกข้อมูลลงในตารางที่มีอยู่แล้ว
        new_entry = user_map(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            tel=tel
        )
        new_entry.save()
        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้ว")
        return redirect('login')
     
    return render(request, 'registration.html')

def generate_user_id():
    # นับจำนวนผู้ใช้ทั้งหมดที่มีอยู่แล้ว
    count = user_map.objects.count() + 1  # ลำดับที่ 1, 2, 3, ...
    
    # สร้างเลข user_id โดยต่อเลข 164 กับลำดับที่มีความยาว 7 หลัก
    user_id = f"164{count:07d}"  # เช่น 1640000001, 1640000002
    return user_id
