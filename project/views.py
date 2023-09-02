from datetime import datetime
import random
import string
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from team.models import TeamMember
from .models import Project, DeletedProject, Team, User, Document, Folder
from message.models import Report


def create_project(request):
    project_name = request.POST.get('project_name')
    team_id = request.POST.get('team_id')

    username = request.session.get('username')
    user = User.objects.get(username=username)
    team = get_object_or_404(Team, id=team_id)
    if Project.objects.filter(team=team, name=project_name).exists():
        result = {'result': 1, 'message': '该项目名称已被使用'}
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
    project_id = request.GET.get('project_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    project = get_object_or_404(Project, id=project_id)
    project.is_deleted = True
    project.save()
    DeletedProject.objects.create(project=project, deleted_by=user)
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
            'project_mem': project.team.teammember_set.count()
        }
        project_list.append(project_info)

    result = {'result': 0, 'message': '获取项目列表成功', 'projects': project_list}
    return JsonResponse(result)


def generate_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def create_file(request):
    file_name = request.POST.get('file_name')
    project_id = request.POST.get('project_id')
    team_id = request.POST.get('team_id')
    folder_id = request.POST.get('folder_id')
    username = request.session.get('username')

    # 获取当前登录用户和团队
    user = User.objects.get(username=username)
    team = get_object_or_404(Team, id=team_id)
    project = get_object_or_404(Project, id=project_id)
    doc_code = generate_invite_code()
    while Document.objects.filter(doc_code=doc_code).exists():
        doc_code = generate_invite_code()
    if int(folder_id) > 0:
        document = Document.objects.create(
            team=team,
            project=project,
            title=file_name,
            content='',
            folder=Folder.objects.get(id=folder_id),
            edited_by=user,
            edited_at=timezone.now(),
            is_deleted=False,
            doc_code=doc_code
        )
    else:
        document = Document.objects.create(
            team=team,
            project=project,
            title=file_name,
            content='',
            edited_by=user,
            edited_at=timezone.now(),
            is_deleted=False,
            doc_code=doc_code
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
    documents = Document.objects.filter(project_id=project_id, is_deleted=False, folder=None)

    files = []
    for document in documents:
        if document.edited_by is None:
            files.append({
                'file_id': document.id,
                'file_name': document.title,
                'file_editor': '游客',
                'file_edit_time': document.edited_at.strftime('%Y-%m-%d')
            })
        else:
            files.append({
                'file_id': document.id,
                'file_name': document.title,
                'file_editor': document.edited_by.username,
                'file_edit_time': document.edited_at.strftime('%Y-%m-%d')
            })
    folders = []
    for folder in Folder.objects.filter(project_id=project_id):
        folders.append({
            'folder_id': folder.id,
            'folder_name': folder.name
        })
    result = {'result': 0, 'message': '获取列表成功', 'files': files, 'folders': folders}
    return JsonResponse(result)


def doc_at(request):
    receiver_name = request.POST.get('username')
    sender_name = request.session['username']
    doc_id = request.POST.get('doc_id')
    team_id = Document.objects.get(id=doc_id).team.id
    if receiver_name == '所有人':
        team_member_list = TeamMember.objects.filter(team_id=team_id)
        for team_member in team_member_list:
            receiver = User.objects.get(id=team_member.member.id)
            if receiver.username == sender_name:
                continue
            sender = User.objects.get(username=sender_name)
            message = Report.objects.create(user=sender, receiver=receiver, doc_id=doc_id)
            message.save()
        result = {'result': 0, 'message': '@成功'}
        return JsonResponse(result)
    else:
        receiver = User.objects.get(username=receiver_name)
        sender = User.objects.get(username=sender_name)
        message = Report.objects.create(user=sender, receiver=receiver, doc_id=doc_id)
        message.save()
        result = {'result': 0, 'message': '@成功'}
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


def get_single_project(request):
    team_id = request.GET.get('team_id')
    project_id = request.GET.get('project_id')

    try:
        project = Project.objects.get(id=project_id, team__id=team_id)
    except Project.DoesNotExist:
        result = {'result': 1, 'message': '项目不存在'}
        return JsonResponse(result)

    project_info = {
        'project_name': project.name,
        'project_team': project.team.name,
        'project_creator': project.created_by.username,
        'project_create_time': project.created_at.strftime('%Y-%m-%d')
    }

    result = {'result': 0, 'message': '获取项目信息成功', 'project': project_info}
    return JsonResponse(result)


def copy_project(request):
    project_id = request.POST.get('project_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    project = Project.objects.get(id=project_id)
    name_copy = project.name + '-副本'
    if Project.objects.filter(name=name_copy).exists():
        name_copy += '('
        i = 1
        while Project.objects.filter(name=name_copy + str(i) + ')').exists():
            i = i + 1
        name_copy += str(i) + ')'
    project_copy = Project.objects.create(team=project.team, created_by=user, name=name_copy)
    for folder in Folder.objects.filter(project=project):
        Folder.objects.create(name=folder.name, project=project_copy)

    for doc in Document.objects.filter(project=project, is_deleted=False):
        doc_copy = Document.objects.create(project=project_copy, team=doc.team, title=doc.title, content=doc.content, edited_by=doc.edited_by)
        if doc.folder is not None:
            doc_copy.folder = Folder.objects.get(name=doc.folder.name, project=project_copy)
            doc_copy.save()
    result = {'result': 0, 'message': '复制成功'}
    return JsonResponse(result)

def create_folder(request):
    project_id = request.POST.get('project_id')
    folder_name = request.POST.get('folder_name')
    if Folder.objects.filter(name=folder_name, project_id=project_id):
        result = {'result': 1, 'message': '文件夹名已存在'}
        return JsonResponse(result)
    username = request.session.get('username')
    project = get_object_or_404(Project, id=project_id)

    # 创建新文件夹
    folder = Folder.objects.create(
        project=project,
        name=folder_name
    )

    result = {'result': 0, 'message': '文件夹创建成功'}
    return JsonResponse(result)


def get_doc_in_folder(request):
    folder_id = request.POST.get('folder_id')
    files = []
    for document in Document.objects.filter(folder_id=folder_id, is_deleted=False):
        if document.edited_by is None:
            files.append({
                'file_id': document.id,
                'file_name': document.title,
                'file_editor': '游客',
                'file_edit_time': document.edited_at.strftime('%Y-%m-%d')
            })
        else:
            files.append({
                'file_id': document.id,
                'file_name': document.title,
                'file_editor': document.edited_by.username,
                'file_edit_time': document.edited_at.strftime('%Y-%m-%d')
            })
    result = {'result': 0, 'message': '获取文件列表成功', 'files': files}
    return JsonResponse(result)


def search_project(request):
    team_id = request.POST.get('team_id')
    keyword = request.POST.get('keyword')
    project_list = []
    for project in Project.objects.filter(team_id=team_id, name__icontains=keyword):
        project_info = {
            'project_id': project.id,
            'project_name': project.name,
            'project_creator': project.created_by.username,
            'project_create_time': project.created_at.strftime('%Y-%m-%d'),
            'project_mem': project.team.teammember_set.count()
        }
        project_list.append(project_info)

    result = {'result': 0, 'message': '获取项目列表成功', 'projects': project_list}
    return JsonResponse(result)

def delete_folder(request):
    folder_id = request.POST.get('folder_id')
    folder = get_object_or_404(Folder, id=folder_id)
    # files = Document.objects.filter(folder=folder)
    # for file in files:
    #     file.is_deleted = True
    #     file.save()
    folder.delete()
    result = {'result': 0, 'message': '文件夹删除成功'}
    return JsonResponse(result)


def get_invite_doc_link(request):
    doc_id = request.POST.get('doc_id')
    try:
        doc = Document.objects.get(id=doc_id)
        doc_code = doc.doc_code
        full_invite_code = f"http://82.157.165.72/invite_doc/{doc_code}"
        result = {'result': 0, 'message': '成功获得邀请链接', 'invite_link': full_invite_code}
        return JsonResponse(result)
    except Document.DoesNotExist:
        result = {'result': 1, 'message': '文件不存在'}
        return JsonResponse(result)
    
    
def set_guest_editable(request):
    doc_id = request.POST.get('doc_id')
    guest_editable = request.POST.get('guest_editable')
    doc = Document.objects.get(id=doc_id)
    doc.guest_editable = guest_editable
    doc.save()
    result = {'result': 0, 'message': '更改权限成功'}
    return JsonResponse(result)


def get_guest_editable(request):
    doc_id = request.POST.get('doc_id')
    guest_editable = Document.objects.get(id=doc_id).guest_editable
    result = {'result': 0, 'message': '获取成功', 'guest_editable': guest_editable}
    return JsonResponse(result)
    

def get_team_id_by_doc_id(request):
    doc_id = request.POST.get('doc_id')
    team_id = Document.objects.get(id=doc_id).team.id
    result = {'result': 0, 'message': '获取成功', 'team_id': team_id}
    return JsonResponse(result)


def create_page(request):
    pass


def get_page_list(request):
    pass


def delete_page(request):
    pass


def save_page(request):
    pass


def read_page(request):
    pass