from django.urls import path
from . import views

# 设置路由器信息，保证页面的正常访问
urlpatterns = [
    path('login/', views.login, name= 'login'),
    path('login_for_model/', views.login_for_model, name= 'login_for_model'),
    path('register/', views.register, name= 'register'),
    path('login_out/', views.login_out, name= 'login_out'),
    path('user_info/', views.user_info, name= 'user_info'),
    path('change_nickname', views.change_nickname, name='change_nickname'),
    path('bind_email', views.bind_email, name='bind_email'),
    path('bind_email_code', views.send_verification_code, name='bind_email_code'),
    path('change_passwd', views.change_passwd, name='change_passwd'),
    path('forget_passwd', views.forget_passwd, name='forget_passwd'),
]


