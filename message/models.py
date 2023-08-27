from django.db import models

from chat.models import GroupChatMessage
from team.models import Team
from user.models import User


# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # chat_message = models.ForeignKey(GroupChatMessage, blank=True, null=True, on_delete=models.CASCADE)
    # text_message = models.ForeignKey(, blank=True, null=True)
    chat_id = models.IntegerField(default=0)  # 如果不为0，即和团队编号相同
    doc_id = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def get_content(self):
        if self.chat_id != 0:
            content = self.user.username + ' 在' + Team.objects.get(id=self.chat_id).name + ' 的群聊中@了你'
            return content
        else:
            content = '内容暂时无法显示'
            return content

    def to_dic(self):
        result = {
            'id': self.id,
            'sender': self.user.username,
            'content': self.get_content(),
            'time': self.created_at,
            'is_read': self.is_read
        }
        return result
