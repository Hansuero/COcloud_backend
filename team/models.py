from django.db import models

from user.models import User


class Team(models.Model):
    name = models.CharField('团队名', max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 创建者
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    invite_code = models.CharField('邀请码', max_length=16)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    TEAM_ROLES = (
        ('admin', '团队管理员'),
        ('member', '普通成员'),
        ('creator', '团队创建者'),
    )


    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # 团队
    member = models.ForeignKey(User, on_delete=models.CASCADE)  # 团队成员
    nikename = models.CharField(max_length=16,blank=True)  # 成员在该团队的昵称
    role = models.CharField(max_length=10, choices=TEAM_ROLES, default='member')  # 成员职位
    join_at = models.DateTimeField(auto_now_add=True)  # 加入时间

    def __str__(self):
        return f"{self.member.username} - {self.team.name}"
# Create your models here.
