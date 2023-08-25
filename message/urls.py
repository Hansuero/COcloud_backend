from django.urls import path
from message.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('read_allmessage', read_allmessage),
    path('delete_message', delete_message),
    path('delete_allmessage', delete_allmessage),

]