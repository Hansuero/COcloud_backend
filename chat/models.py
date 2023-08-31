from django.db import models

from team.models import Team
from user.models import User


# Create your models here.
class GroupChatMessage(models.Model):
    group = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class PrivateChatMessage(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE) # 这个是发送者
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1') # 这个是接收者
    text_content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class GroupChatMention(models.Model):
    message = models.ForeignKey(GroupChatMessage, on_delete=models.CASCADE)
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE)
