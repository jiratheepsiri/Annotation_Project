from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import bcrypt

class user_map(models.Model):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True) # Field for user_id
    username = models.CharField(max_length=150, unique=True,db_column='user_username')
    email = models.EmailField(max_length=255, unique=True,db_column='user_email')
    password = models.CharField(max_length=255,db_column='user_pwd')
    tel = models.CharField(max_length=10,db_column='user_tel')
    user_role = models.CharField(max_length=10,db_column='user_role')
    
    class Meta:
        db_table = 'user'  # กำหนดชื่อตารางเป็น 'user'
        managed = True

class Users(models.Model):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True, db_column='user_id')
    username = models.CharField(max_length=150, unique=True, db_column='user_username')
    password = models.CharField(max_length=255, db_column='user_pwd')
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    class Meta:
        db_table = 'user'  # Use your actual table name in MySQL
        managed = False

    @property
    def is_authenticated(self):
        return True  # Custom implementation for your Users model

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self):
        return self.username

class ProposedText(models.Model):
    text_id = models.AutoField( unique=True, primary_key=True, db_column='text_id')
    propose_t_admin_id = models.CharField(max_length=10, db_column='propose_t_admin_id')
    proposed_t_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    propose_t_uploaded_id = models.CharField(max_length=10, db_column='propose_t_uploaded_id')
    uploaded_id = models.CharField(max_length=10, db_column='uploaded_id')
    user_proposed_text = models.TextField(max_length=255, db_column='word_text')
    word_status = models.CharField(max_length=15, db_column='word_status', default='รออนุมัติ')
    word_class = models.CharField(max_length=16, db_column='word_class')
    word_class_type = models.CharField(max_length=20, db_column='word_class_type')

    class Meta:
        db_table = 'proposed_text'  # Use your desired table name in MySQL
        managed = True


