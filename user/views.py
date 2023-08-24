import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404

from COcloud_backend.settings import BASE_DIR
from user.models import User
from utils.utils import *


def register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if User.objects.filter(username=username).exists():
        result = {'result': 1, 'message': r'用户名已存在'}
        return JsonResponse(result)

    email = request.POST.get('email', '')
    photo_url = os.path.join(BASE_DIR, 'photo', 'default.jpg')

    user = User.objects.create(username=username, password=password, email=email, photo_url=photo_url)
    user.save()
    # request.session['username'] = username
    # request.session.set_expiry(3600)
    result = {'result': 0, 'message': r'注册成功'}
    return JsonResponse(result)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        result = {'result': 1, 'message': r'用户名或密码错误'}
        return JsonResponse(result)
    user = User.objects.get(username=username)
    if user.password == password:
        request.session['username'] = username
        user = User.objects.get(username=username)
        user.is_login = True
        user.save()
        result = {'result': 0, 'message': r'登录成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'用户名或密码错误'}
        return JsonResponse(result)


def logout(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    user.is_login = False
    user.save()
    request.session.flush()
    result = {'result': 0, 'message': r'注销成功'}
    return JsonResponse(result)


username_verify = ''
email_verify = ''
code = 0


def verify_identity(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    if User.objects.filter(username=username, email=email).exists():
        result = {'result': 0, 'message': r'确认成功'}
        global username_verify
        username_verify = username
        global email_verify
        email_verify = email
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'用户名或邮箱错误'}
        username_verify = ''
        email_verify = ''
        return JsonResponse(result)


def send_code(request):
    try:
        global code
        code = send_email(email_verify)
        result = {'result': 0, 'message': r'发送成功'}
        return JsonResponse(result)
    except:
        code = 0
        result = {'result': 1, 'message': r'发送失败'}
        return JsonResponse(result)


def verify_code(request):
    global code
    code_to_verify = request.POST.get('code')
    if code == code_to_verify:
        code = 0
        result = {'result': 0, 'message': '验证码正确'}
        return JsonResponse(result)
    else:
        code = 0
        result = {'result': 1, 'message': '验证码错误'}
        return JsonResponse(result)


def change_password(request):
    global username_verify, email_verify
    password = request.POST.get('password')
    user = User.objects.get(username=username_verify)
    user.password = password
    user.save()
    username_verify = ''
    email_verify = ''
    result = {'result': 0, 'message': '修改成功'}
    return JsonResponse(result)


def get_userinfo(request):
    if request.method == 'GET':
        username = request.session.get('username')  # 使用 get() 方法避免 KeyError
        if username is None:
            result = {'result': 1, 'message': r'未登录'}
            return JsonResponse(result)

        user = User.objects.get(username=username)
        email = user.email
        photo_url = user.photo_url
        result = {
            'result': 0,
            'message': '返回成功',
            'username': username,
            'email': email,
            'photo_url': photo_url,
        }
        return JsonResponse(result)
