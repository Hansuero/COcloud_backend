import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from .models import Document
from user.models import User
from team.models import Team
CONN_LIST = [[] for i in range(100)]


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message): # message {'type': 'websocket.receive', 'text': {'username': '你爹', 'msg': i}}
        print("开始链接文档...")
        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()
        self.doc_id = int(self.scope['url_route']['kwargs']['doc_id'])
        print('文档编号', self.doc_id)
        doc = Document.objects.get(id=self.doc_id)
        
        res = {'type': 'websocket.receive', 'text': {'content': doc.content}}
        print(res)
        self.send(json.dumps(res))
        CONN_LIST[self.doc_id].append(self)

    def websocket_receive(self, message):
        text = eval((message['text']))
        
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        content = text['content']
        editer_name = text['username']
        editer = User.objects.get(username=editer_name)
        document = Document.objects.get(id=self.doc_id)
        document.content = content
        document.edited_by = editer
        document.save()
        res = {'type': 'websocket.receive', 'text': {'content': content}}
        print(res)
        for conn in CONN_LIST[self.doc_id]:
            conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        #room_id = message['text']['room_id']
        CONN_LIST[self.doc_id].remove(self)
        raise StopConsumer()