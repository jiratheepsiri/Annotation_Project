from django.db import models

class user_map(models.Model):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True) # Field for user_id
    username = models.CharField(max_length=150, unique=True,db_column='user_username')
    email = models.EmailField(max_length=255, unique=True,db_column='user_email')
    password = models.CharField(max_length=255,db_column='user_pwd')
    tel = models.CharField(max_length=10,db_column='user_tel')
    
    class Meta:
        db_table = 'user'  # กำหนดชื่อตารางเป็น 'user'
        managed = False
# Create your models here.
