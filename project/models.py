from django.db import models
from team.models import Team, TeamMember
from user.models import User


class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='所属团队')
    name = models.CharField('项目名', max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=' 项目创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_deleted = models.BooleanField('是否删除', default=False)

    def __str__(self):
        return self.name


class DeletedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='删除者')
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deleted:{self.project.name}"


class Folder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Document(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=255)
    content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)  # 最后修改者
    edited_at = models.DateTimeField(auto_now=True)  # 最后修改时间
    is_deleted = models.BooleanField(default=False)  # 添加软删除字段
    doc_code = models.CharField('文档邀请码', max_length=16)
    guest_editable = models.BooleanField(default=False)


class Page(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    canvasStyle = models.TextField()
    canvasData = models.TextField()

