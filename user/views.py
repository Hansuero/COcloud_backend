import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from COcloud_backend.settings import BASE_DIR
from user.models import User


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if User.objects.filter(username=username).exists():
            result = {'result': 2, 'message': r'用户已存在！'}
            return JsonResponse(result)


        email = request.POST.get('email', '')
        photo_url = os.path.join(BASE_DIR, 'photo', 'default.jpg')

        user = User.objects.create(username=username, password=password, email=email, photo_url=photo_url)
        user.save()
        request.session['username'] = username
        request.session.set_expiry(3600)
        result = {'result': 0, 'message': r'注册成功！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r"请求方式错误！"}
        return JsonResponse(result)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username):
            result = {'result': 2, 'message': r'查无此人！'}
            return JsonResponse(result)
        user = User.objects.get(username=username)
        if user.password == password:
            request.session['username'] = username
            request.session.set_expiry(3600)
            result = {'result': 0, 'message': r'登录成功！'}
            return JsonResponse(result)
        else:
            result = {'result': 3, 'message': r'密码错误！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def logout(request):
    request.session.flush()
    result = {'result': 0, 'message': r'注销成功！'}
    return JsonResponse(result)


def get_userinfo(request):
        if request.method == 'GET':
            username = request.session.get('username')  # 使用 get() 方法避免 KeyError
            if username is None:
                result = {'result': -1, 'message': r'未登录！'}
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






# Create your views here.
