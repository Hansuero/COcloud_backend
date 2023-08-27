from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Project, DeletedProject, Team, User, Document


def create_project(request):
    project_name = request.POST.get('project_name')
    team_id = request.POST.get('team_id')

    username = request.session.get('username')
    user = User.objects.get(username=username)
    team = get_object_or_404(Team, id=team_id)
    project = Project.objects.create(created_by=user, team=team, name=project_name)
    result = {'result': 0, 'message': '项目创建成功'}
    return JsonResponse(result)


def rename_project(request):
    project_id = request.POST.get('project_id')
    project_new_name = request.POST.get('project_new_name')
    project = get_object_or_404(Project, id=project_id)
    project.name = project_new_name
    project.save()
    result = {'result': 0, 'message': '项目重命名成功'}
    return JsonResponse(result)


def delete_project(request):
    project_id = request.POST.get('project_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    project = get_object_or_404(Project, id=project_id)
    project.is_deleted = True
    project.save()
    DeletedProject.objects.create(project=project,deleted_by=user)
    result = {'result': 0, 'message': '项目删除成功'}
    return JsonResponse(result)


def get_project(request):
    team_id = request.GET.get('team_id')

    projects = Project.objects.filter(team_id=team_id, is_deleted=False)

    project_list = []
    for project in projects:
        project_info = {
            'project_id': project.id,
            'project_name': project.name,
            'project_creator': project.created_by.username,
            'project_create_time': project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'project_member': project.team.teammember_set.count()
        }
        project_list.append(project_info)

    result = {'result': 0, 'message': '获取项目列表成功', 'project_list': project_list}
    return JsonResponse(result)


def create_file(request):
    file_name = request.POST.get('file_name')
    project_id = request.POST.get('project_id')
    team_id = request.POST.get('team_id')
    username = request.session.get('username')

    # 获取当前登录用户和团队
    user = User.objects.get(username=username)
    team = get_object_or_404(Team, id=team_id)
    project = get_object_or_404(Project, id=project_id)

    # 创建新文档
    document = Document.objects.create(
        team=team,
        project=project,
        title=file_name,
        content='',
        edited_by=user,
        edited_at=timezone.now()
    )

    result = {'result': 0, 'message': '文档创建成功'}
    return JsonResponse(result)
# Create your views here.
