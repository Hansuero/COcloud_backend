from django.db.models import Model
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from message.models import Report
from .models import Team, TeamMember
from user.models import User


def get_memberlist(request):
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        username = request.session.get('username')
        user = User.objects.get(username=username)

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            result = {'result': 1, 'message': '团队不存在'}
            return JsonResponse(result)

        if not TeamMember.objects.filter(team=team, member=user).exists():
            result = {'result': 2, 'message': '你不是该团队成员'}
            return JsonResponse(result)

        members = TeamMember.objects.filter(team=team)
        member_list = []

        for member in members:
            member_info = {
                'teammember_id': member.member.id,
                'photo_url': member.member.photo_url_out,
                'nickname': member.nickname,
                'email': member.member.email,
                'role': '0' if member.role == 'creator' else '2' if member.role == 'member' else '1',
                'rolename': '团队创建者' if member.role == 'creator' else '团队管理员' if member.role == 'admin' else '普通成员'
            }
            member_list.append(member_info)

        result = {
            'result': 0,
            'message': '获取团队成员列表成功',
            'memberlist': member_list
        }
        return JsonResponse(result)

    else:
        result = {'result': 1, 'message': '请求方式错误'}
        return JsonResponse(result)


def delete_member(request):
    teammember_id = request.POST.get('teammember_id')
    team_id = request.POST.get('team_id')
    try:
        TeamMember.objects.get(member_id=teammember_id, team_id=team_id).delete()
        result = {'result': 0, 'message': '删除成功'}
        return JsonResponse(result)
    except TeamMember.DoesNotExist:
        result = {'result': 1, 'message': '用户不存在'}
        return JsonResponse(result)


def change_role(request):
    team_id = request.POST.get('team_id')
    teammember_id = request.POST.get('teammember_id')
    new_role_id = request.POST.get('new_role')
    new_role = ''
    if new_role_id == '0':
        new_role = 'creator'
    elif new_role_id == '1':
        new_role = 'admin'
    else:
        new_role = 'member'

    try:
        team = Team.objects.get(id=team_id)
        user = User.objects.get(id=teammember_id)
        teammember = TeamMember.objects.get(team=team, member=user)
        teammember.role = new_role
        print(new_role)
        teammember.save()
        result = {'result': 0, 'message': '修改权限成功'}
        return JsonResponse(result)
    except TeamMember.DoesNotExist:
        result = {'result': 1, 'message': '成员不存在'}
        return JsonResponse(result)


def get_role(request):
    team_id = request.POST.get('team_id')
    username = request.session['username']
    teammember_id = User.objects.get(username=username).id
    team = Team.objects.get(id=team_id)
    user = User.objects.get(id=teammember_id)
    role = TeamMember.objects.get(team=team, member=user).role
    if role == 'creator':
        result = {'result': 0, 'message': '获取权限成功', 'role': 0}
        return JsonResponse(result)
    elif role == 'admin':
        result = {'result': 0, 'message': '获取权限成功', 'role': 1}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '获取权限成功', 'role': 2}
        return JsonResponse(result)


def get_invite_link(request):
    team_id = request.POST.get('team_id')
    try:
        team = Team.objects.get(id=team_id)
        invite_code = team.invite_code
        full_invite_code = f"http://82.157.165.72/invite/{invite_code}"
        result = {'result': 0, 'message': '成功获得邀请链接', 'invite_link': full_invite_code}
        return JsonResponse(result)
    except Team.DoesNotExist:
        result = {'result': 1, 'message': '团队不存在'}
        return JsonResponse(result)


def invite(request):
    invite_code = request.POST.get('sign')
    try:
        team = Team.objects.get(invite_code=invite_code)
    except Team.DoesNotExist:
        result = {'result': 1, 'message': '无效的邀请链接'}
        return JsonResponse(result)
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.get(username=username, password=password)
        if TeamMember.objects.filter(team=team, member=user).exists():
            result = {'result': 1, 'message': '用户已是团队成员'}
            return JsonResponse(result)
        else:

            TeamMember.objects.create(team=team, member=user, role='member', nickname=user.username)
            result = {'result': 0, 'message': '成功加入团队'}
            return JsonResponse(result)
    except User.DoesNotExist:
            result = {'result': 1, 'message': '用户名或密码错误'}
            return JsonResponse(result)

def chat_at(request):
    receiver_name = request.POST.get('username')
    sender_name = request.session['username']
    team_id = request.POST.get('team_id')
    if receiver_name == '所有人':
        team_member_list = TeamMember.objects.filter(team_id=team_id)
        for team_member in team_member_list:
            receiver = User.objects.get(id=team_member.member.id)
            if receiver.username == sender_name:
                continue
            sender = User.objects.get(username=sender_name)
            message = Report.objects.create(user=sender, receiver=receiver, chat_id=team_id)
            message.save()
        result = {'result': 0, 'message': '@成功'}
        return JsonResponse(result)
    else:
        receiver = User.objects.get(username=receiver_name)
        sender = User.objects.get(username=sender_name)
        message = Report.objects.create(user=sender, receiver=receiver, chat_id=team_id)
        message.save()
        result = {'result': 0, 'message': '@成功'}
        return JsonResponse(result)


def get_namelist(request):
    team_id = request.POST.get('team_id')
    username = request.session.get('username')
    if username is None:
        result = {'result': 3, 'message': '未登录'}
        return JsonResponse(result)
    user = User.objects.get(username=username)
    

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        result = {'result': 1, 'message': '团队不存在'}
        return JsonResponse(result)

    if not TeamMember.objects.filter(team=team, member=user).exists():
        result = {'result': 2, 'message': '你不是该团队成员'}
        return JsonResponse(result)

    members = TeamMember.objects.filter(team=team)
    namelist = []

    for member in members:
        namelist.append(member.member.username)
    result = {
        'result': 0,
        'message': '获取成员用户名列表成功',
        'namelist': namelist
    }
    return JsonResponse(result)
