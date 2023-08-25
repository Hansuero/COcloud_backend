from django.db import models

from team.models import Team
from user.models import User


# Create your models here.
class GroupChatMessage(models.Model):
    group = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class GroupChatMention(models.Model):
    message = models.ForeignKey(GroupChatMessage, on_delete=models.CASCADE)
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE)
