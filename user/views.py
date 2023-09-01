import os
import random
import string

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from team.models import TeamMember, Team
from COcloud_backend.settings import BASE_DIR
from user.models import User
from utils.utils import *


def register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if User.objects.filter(username=username).exists():
        result = {'result': 1, 'report': r'用户名已存在'}
        return JsonResponse(result)

    email = request.POST.get('email', '')
    photo_url = os.path.join(BASE_DIR, 'photo', 'default.jpg')

    user = User.objects.create(username=username, password=password, email=email, photo_url=photo_url)
    user.save()
    # request.session['username'] = username
    # request.session.set_expiry(3600)
    result = {'result': 0, 'report': r'注册成功'}
    return JsonResponse(result)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        result = {'result': 1, 'report': r'用户名或密码错误'}
        return JsonResponse(result)
    user = User.objects.get(username=username)
    if user.password == password:
        request.session['username'] = username
        user = User.objects.get(username=username)
        user.is_login = True
        user.save()
        result = {'result': 0, 'report': r'登录成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'report': r'用户名或密码错误'}
        return JsonResponse(result)


def logout(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    user.is_login = False
    user.save()
    request.session.flush()
    result = {'result': 0, 'report': r'注销成功'}
    return JsonResponse(result)


username_verify = ['' for i in range(100)]
email_verify = ['' for i in range(100)]
code_list = [0 for i in range(100)]


def verify_identity(request):
    username = request.POST.get('username')
    
    email = request.POST.get('email')
    if User.objects.filter(username=username, email=email).exists():
        user_id = User.objects.get(username=username).id
        result = {'result': 0, 'report': r'确认成功'}
        global username_verify
        username_verify[user_id] = username
        global email_verify
        email_verify[user_id] = email
        return JsonResponse(result)
    else:
        result = {'result': 1, 'report': r'用户名或邮箱错误'}
        return JsonResponse(result)


def send_code(request):
    username = request.POST.get('username')
    user_id = User.objects.get(username=username).id
    try:
        global code_list
        code_list[user_id] = send_email(email_verify[user_id])
        result = {'result': 0, 'report': r'发送成功' }
        return JsonResponse(result)
    except:
        result = {'result': 1, 'report': r'发送失败'}
        return JsonResponse(result)


def verify_code(request):
    global code_list
    username = request.POST.get('username')
    user_id = User.objects.get(username=username).id
    code_to_verify = request.POST.get('code')
    print('name:', username, 'code:', code_list[user_id], 'code_to_verify:', code_to_verify)
    if code_list[user_id] == code_to_verify:
        result = {'result': 0, 'report': '验证码正确'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'report': '验证码错误'}
        return JsonResponse(result)


def change_password(request):
    global username_verify, email_verify
    username = request.POST.get('username')
    user_id = User.objects.get(username=username).id
    password = request.POST.get('password')
    user = User.objects.get(username=username_verify[user_id])
    user.password = password
    user.save()
    result = {'result': 0, 'report': '修改成功'}
    return JsonResponse(result)


def get_userinfo(request):
    if request.method == 'POST':
        username = request.session.get('username')  # 使用 get() 方法避免 KeyError
        if username is None:
            result = {'result': 1, 'report': r'未登录'}
            return JsonResponse(result)

        user = User.objects.get(username=username)
        team_id = request.POST.get('teamid')
        team = Team.objects.get(id=team_id)
        nickname = TeamMember.objects.get(team=team, member=user).nickname
        email = user.email
        photo_url_out = user.photo_url_out
        result = {
            'result': 0,
            'report': '返回成功',
            'username': username,
            'email': email,
            'photo_url': photo_url_out,
            'nickname': nickname
        }
        return JsonResponse(result)


def upload_avatar(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    avatar = request.FILES.get('avatar')  # 获取上传的头像文件

    if avatar:  # 如果上传了头像文件
        # 生成头像文件的保存路径
        _, ext = os.path.splitext(avatar.name)
        avatar_path = os.path.join(BASE_DIR, 'avatar', f'{user.username}_avatar.png')

        # 保存头像文件到指定路径
        with open(avatar_path, 'wb') as file:
            for chunk in avatar.chunks():
                file.write(chunk)

        # 更新用户的头像路径
        user.photo_url = avatar_path
        user.photo_url_out = 'http://82.157.165.72:8888/avatar/' + f'{user.username}_avatar.png'
        user.save()
        result = {'result': 0, 'report': r'上传成功'}
        return JsonResponse(result)


def get_teamlist(request):
    if request.method == 'GET':
        username = request.session.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            result = {'result': 1, 'report': '用户不存在'}
            return JsonResponse(result)

        team_memberships = TeamMember.objects.filter(member=user)

        team_list = []
        for membership in team_memberships:
            team_info = {

                'team_name': membership.team.name,
                'team_id': membership.team.id,
                # 'role': membership.get_role_display(),
                # You can include other team information here
            }
            team_list.append(team_info)

        result = {
            'result': 0,
            'report': '获取参与团队成功',
            'teamlist': team_list,
        }
        return JsonResponse(result)


def generate_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        username = request.session.get('username')
        user = User.objects.get(username=username)
        invite_code = generate_invite_code()
        while Team.objects.filter(invite_code=invite_code).exists():
            invite_code = generate_invite_code()

        if Team.objects.filter(name=team_name).exists():
            result = {'result': 1, 'report': '团队名已存在'}
            return JsonResponse(result)

        team = Team.objects.create(name=team_name, created_by=user, invite_code=invite_code)

        TeamMember.objects.create(team=team, member=user, role='creator', nickname=user.username)

        result = {'result': 0, 'report': '团队创建成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'report': '请求方式错误'}
        return JsonResponse(result)


def upload_nickname(request):
    team_id = request.POST.get('teamid')
    nickname = request.POST.get('nickname')
    username = request.session['username']
    user = User.objects.get(username=username)
    try:
        team = Team.objects.get(id=team_id)
        teammember = TeamMember.objects.get(member=user, team=team)
        teammember.nickname = nickname
        teammember.save()
        result = {'result': 0, 'report': '修改成功'}
        return JsonResponse(result)
    except TeamMember.DoesNotExist:
        result = {'result': 1, 'report': '用户不存在'}
        return JsonResponse(result)


def get_id(request):
    username = request.POST.get('username')
    id = User.objects.get(username=username).id
    print(username, ' 的id是 ',id)
    result = {'result': 0, 'id': id}
    return JsonResponse(result)