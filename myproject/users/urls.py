from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('mainlogin/', views.mainlogin, name='mainlogin'),
    path('annotatepage/', views.annotatepage, name='annotatepage'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('texttopost/', views.texttopost, name='texttopost'),
    path('texttopostFile/', views.texttopostFile, name='texttopostFile'),
    path('txtverify/', views.txtverify, name='txtverify'),
    path('txtverifyFile/', views.txtverifyFile, name='txtverifyFile'),
    path('registration/', views.registration, name='registration'),
]
