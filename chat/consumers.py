import json
from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from .models import GroupChatMessage, PrivateChatMessage
from user.models import User
from team.models import Team
CONN_LIST = [[] for i in range(100)]
PCONN_LIST = [[] for i in range(100)]


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message): # message {'type': 'websocket.receive', 'text': {'username': '你爹', 'msg': i}}
        print("开始群聊链接...")
        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()
        self.room_id = int(self.scope['url_route']['kwargs']['room_id'])
        print('房间号', self.room_id)
        message_list = GroupChatMessage.objects.filter(group_id=self.room_id).order_by('timestamp')
        for msg in message_list:
            res = {'type': 'websocket.receive', 'text': {'username': msg.sender.username, 'msg': msg.text_content}}
            self.send(json.dumps(res))
        #for i in range(100):
        #    res = {'type': 'websocket.receive', 'text': {'username': '你爹', 'msg': i}}
        #    self.send(json.dumps(res))
        CONN_LIST[self.room_id].append(self)

    def websocket_receive(self, message):
        text = eval((message['text']))
        
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        username = text['username']
        text_content = text['msg']
        sender = User.objects.get(username=username)
        group = Team.objects.get(id=self.room_id)
        group_chat_message = GroupChatMessage.objects.create(group=group, sender=sender, text_content=text_content)
        group_chat_message.save()
        res = message
        for conn in CONN_LIST[self.room_id]:
            conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        #room_id = message['text']['room_id']
        CONN_LIST[self.room_id].remove(self)
        raise StopConsumer()
class PrivateChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message): # message {'type': 'websocket.receive', 'text': {'username': '你爹', 'msg': i}}
        print("开始私聊链接...")
        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()
        self.user_id_1 = int(self.scope['url_route']['kwargs']['userid_1'])
        self.user_id_2 = int(self.scope['url_route']['kwargs']['userid_2'])
        print('自己：', self.user_id_1, ' 对方：',self.user_id_2)
        message_list = PrivateChatMessage.objects.filter(Q(user1_id=self.user_id_1, user2_id=self.user_id_2)|Q(user1_id=self.user_id_2, user2_id=self.user_id_1)).order_by('timestamp')
        for msg in message_list:
            res = {'type': 'websocket.receive', 'text': {'username': msg.user1.username, 'msg': msg.text_content}}
            self.send(json.dumps(res))
        #for i in range(100):
        #    res = {'type': 'websocket.receive', 'text': {'username': '你爹', 'msg': i}}
        #    self.send(json.dumps(res))
        PCONN_LIST[self.user_id_1].append(self)

    def websocket_receive(self, message):
        text = eval((message['text']))
        print('text:', text)
        
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        username = text['username']
        sender_id = User.objects.get(username=username).id
        print('username:', username)
        receiver_name = ''
        username_1 = User.objects.get(id=self.user_id_1)
        print('username_1:', username_1)
        username_2 = User.objects.get(id=self.user_id_2)
        print('username_2:', username_2)
        receiver_name = username_2
        text_content = text['msg']
        sender = User.objects.get(username=username)
        receiver = User.objects.get(username=receiver_name)
        private_chat_message = PrivateChatMessage.objects.create(user1=sender, user2=receiver,text_content=text_content)
        private_chat_message.save()
        res = message
        for conn in PCONN_LIST[self.user_id_1]:
        	conn.send(json.dumps(res))
        for conn in PCONN_LIST[self.user_id_2]:
        	conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        #room_id = message['text']['room_id']
        PCONN_LIST[self.user_id_1].remove(self)
        raise StopConsumer()