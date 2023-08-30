from django.db import models
from datetime import datetime
from chat.models import GroupChatMessage
from team.models import Team
from user.models import User
from project.models import Document


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
            content = self.user.username + ' 在团队 ' + Team.objects.get(id=self.chat_id).name + ' 的群聊中@了你'
            return content
        else:
            content = self.user.username + ' 在团队 ' + Document.objects.get(id=self.doc_id).team.name +' 的文档 ' + Document.objects.get(id=self.doc_id).title + ' 中@了你'
            return content

    def time_to_last(self, time):
        now_time = datetime.now().replace(tzinfo=None)
        time = time.replace(tzinfo=None)
        last =now_time  - time
        last_second = int(last.seconds)
        last_minute = int(last_second / 60)
        last_hour = int(last_minute / 60)
        last_day = int(last.days)
        if last_second < 5:
            return '刚刚'
        elif last_second < 60:
            return str(last_second) + '秒前'
        elif last_minute < 60:
            return str(last_minute) + '分钟前'
        elif last_hour < 24:
            return str(last_hour) + '小时前'
        elif last_day < 3:
            return str(last_day) + '天前'
        else:
            return '3天前'
        
    def to_dic(self):
        result = {
            'id': self.id,
            'sender': self.user.username,
            'content': self.get_content(),
            'time': self.time_to_last(self.created_at),
            'is_read': self.is_read
        }
        return result
