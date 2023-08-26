from django.urls import path

from team import views
from team.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('get_memberlist', get_memberlist),
    path('delete_member', delete_member),
    path('change_role', change_role),
    path('get_role', get_role),
    path('get_invite_link', get_invite_link),
    path('invite', views.invite, name='invite'),
]