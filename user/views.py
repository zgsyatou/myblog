import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from .forms import LoginForm, RegisterForm, NicknameChangeForm, BindEmailForm, ChangePasswordForm, ForgetPasswordForm
from .models import Profile


# 定义页面登录的返回的数据
def login_for_model(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)  # 使用内置方法进行创建
            user.save()
            # 清楚验证码
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)

# 退出登录
def login_out(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))

# 用户信息展示
def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == 'POST':
        form = NicknameChangeForm(request.POST, user = request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user = request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = NicknameChangeForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text']  = '确认'
    context['return_back'] = redirect_to
    return render(request, 'form.html', context)

# 绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request = request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清楚验证码
            del request.session['bind_email']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text']  = '确认'
    context['return_back'] = redirect_to
    return render(request, 'user/bind_email.html', context)

# 给邮箱发送验证码
def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for')
    data = {}
    if email != '':
        # 生成验证码
        # ''.join将生成的雅正吗（列表）转换为字符串。
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time <= 60:
             data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                    '电影网站：绑定邮箱',
                    '【电影网站】绑定验证码为：%s，本验证码10分钟内有效。' % code,
                    '645164577@qq.com',
                    [email], 
                    fail_silently=False,
                     )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

# 修改用户的密码
def change_passwd(request):
    redirect_to = reverse('index')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user = request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            # 使用user内置的方法保存修改的密码
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text']  = '确定'
    context['return_back'] = redirect_to
    return render(request, 'form.html', context)

# 未登录忘记密码
def forget_passwd(request):
    redirect_to = reverse('index')
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request = request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email= email)
            user.set_password(new_password)
            user.save()
            # 清楚session
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '忘记密码'
    context['form_title'] = '忘记密码'
    context['submit_text']  = '确认'
    context['return_back'] = redirect_to
    return render(request, 'user/forget_password.html', context)
