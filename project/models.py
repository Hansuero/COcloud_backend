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
# Create your models here.
