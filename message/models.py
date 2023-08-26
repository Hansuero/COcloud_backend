from django.db import models

from chat.models import GroupChatMessage
from user.models import User


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_message = models.ForeignKey(GroupChatMessage, blank=True, null=True, on_delete=models.CASCADE)
    # text_message = models.ForeignKey(, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_content(self):
        if self.chat_message is not None:
            content = self.user.username + ' 在' + self.chat_message.group.name + ' 的群聊中@了你'
            return content
        else:
            # 是项目的@
            pass

    def to_dic(self):
        result = {
            'id': self.id,
            'sender': self.user.username,
            'content': self.get_content(),
            'time': self.created_at,
            'is_read': self.is_read
        }
        return result
