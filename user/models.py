from django.db import models


class User(models.Model):
    ROLES = (
        ('creator', '团队创建者'),
        ('admin', '团队管理员'),
        ('member', '普通成员'),
    )

    username = models.CharField('用户名', max_length=16)
    password = models.CharField('密码', max_length=20)
    email = models.EmailField('邮箱', unique=True)
    role = models.CharField('职位', max_length=10, choices=ROLES)
    created_at = models.DateTimeField('创建日期', auto_now_add=True)
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    is_login = models.BooleanField('登录状态', default=False)

    def __str__(self):
        return self.username
# Create your models here.
