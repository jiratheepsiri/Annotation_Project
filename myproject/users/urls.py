from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('annotatepage/', views.annotatepage, name='annotatepage'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('texttopost.html', views.texttopost, name='texttopost'),
    path('texttopostFile.html', views.texttopostFile, name='texttopostFile'),
    path('txtverify.html', views.txtverify, name='txtverify'),
    path('txtverifyFile.html', views.txtverifyFile, name='txtverifyFile'),
    path('registration/', views.registration, name='registration'),
]
