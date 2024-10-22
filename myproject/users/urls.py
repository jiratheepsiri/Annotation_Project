from django.urls import path
from . import views
from .views import login_view
from .views import texttopost

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('login/accounts/mainlogin/', views.mainlogin, name='mainlogin'),
    path('annotatepage/', views.annotatepage, name='annotatepage'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('login/accounts/texttopost/', texttopost, name='texttopost'),
    path('login/accounts/texttopostFile/', views.texttopostFile, name='texttopostFile'),
    path('login/accounts/txtverify/', views.txtverify, name='txtverify'),
    path('login/accounts/txtverifyFile/', views.txtverifyFile, name='txtverifyFile'),
    path('registration/', views.registration, name='registration'),
    path('login/accounts/annotateselect/', views.annotateselect, name='annotateselect'),
    path('login/accounts/edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/accounts/user_profile/', views.user_profile, name='user_profile')
]
