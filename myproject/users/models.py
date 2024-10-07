from django.db import models
from django.contrib.auth.hashers import check_password


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
    user_id = models.CharField(max_length=10, unique=True, primary_key=True,db_column='user_id') # Field for user_id
    username = models.CharField(max_length=150, unique=True,db_column='user_username')
    password = models.CharField(max_length=255,db_column='user_pwd')

    class Meta:
        db_table = 'user'  # Use your actual table name in MySQL
        managed = False  # Django won’t create or modify this table

    def verify_password(self, raw_password):
        # Verifies the password by comparing the hashed password in the database
        return check_password(raw_password, self.user_pwd)


