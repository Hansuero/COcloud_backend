import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("开始链接...")
        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()

        CONN_LIST.append(self)

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        print('接受的消息', message)
        text = message  # {'type': 'websocket.receive', 'text': '阿斯蒂芬'}
        print("接收到消息-->", text)
        print(('msg' in text['text']))
        res = message
        for conn in CONN_LIST:
            conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        CONN_LIST.remove(self)
        raise StopConsumer()