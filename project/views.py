from datetime import datetime

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
            'project_create_time': project.created_at.strftime('%Y-%m-%d'),
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
        edited_at=timezone.now(),
        is_deleted=False
    )

    result = {'result': 0, 'message': '文档创建成功'}
    return JsonResponse(result)


def delete_file(request):
    file_id = request.POST.get('file_id')
    project_id = request.POST.get('project_id')
    team_id = request.POST.get('team_id')

    document = get_object_or_404(Document, id=file_id, project_id=project_id, team_id=team_id)

    # 设置 is_deleted 为 True
    document.is_deleted = True
    document.save()

    result = {'result': 0, 'message': '文件删除成功'}
    return JsonResponse(result)


def get_content(request):
        file_id = request.GET.get('file_id')

        document = get_object_or_404(Document, id=file_id)

        content = document.content

        result = {'result': 0, 'message': '获取内容成功', 'content': content}
        return JsonResponse(result)


def get_file(request):
    team_id = request.GET.get('team_id')
    project_id = request.GET.get('project_id')

    documents = Document.objects.filter(project_id=project_id, project__team_id=team_id, is_deleted=False)

    files = []
    for document in documents:
        files.append({
            'file_id': document.id,
            'file_name': document.title,
            'file_editor': document.edited_by.username,
            'file_edit_time': document.edited_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    result = {'result': 0, 'message': '获取文件列表成功', 'files': files}
    return JsonResponse(result)


def chat_at(request):
    doc_id = request.POST.get('doc_id')
    username = request.POST.get('username')

    try:
        document = Document.objects.get(id=doc_id)
        user = User.objects.get(username=username)
    except Document.DoesNotExist:
        result = {'result': 1, 'message': '文档不存在'}
        return JsonResponse(result)
    except User.DoesNotExist:
        result = {'result': 1, 'message': '用户不存在'}
        return JsonResponse(result)

    # 在这里执行 @ 功能的逻辑，可以根据实际情况进行实现

    result = {'result': 0, 'message': '@ 成功'}
    return JsonResponse(result)


def cur_edit(request):
    file_id = request.POST.get('file_id')
    user_name = request.POST.get('user_name')
    content = request.POST.get('content')
    project_id = request.POST.get('project_id')
    team_id = request.POST.get('team_id')

    # 根据提供的信息找到对应的文档
    document = get_object_or_404(Document, id=file_id, project__id=project_id, project__team__id=team_id)

    # 更新文档内容和编辑信息
    document.content = content
    document.edited_by = User.objects.get(username=user_name)
    document.edited_at = datetime.now()
    document.save()

    result = {'result': 0, 'message': '文档内容更新成功'}
    return JsonResponse(result)
# Create your views here.
