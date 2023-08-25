from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
                'id': member.member.id,
                'username': member.member.username,
                'email': member.member.email,
                'role': '0' if member.role == 'creator' else '2' if member.role == 'member' else '1'
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

# Create your views here.
