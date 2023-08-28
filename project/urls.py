from django.urls import path

from project.views import *

urlpatterns = [
    path('create_project', create_project),
    path('rename_project', rename_project),
    path('delete_project', delete_project),
    path('get_project', get_project),
    path('create_file', create_file),
    path('delete_file', delete_file),
    path('get_content', get_content),
    path('get_file', get_file),
    path('chat_at', chat_at),
    path('cur_edit', cur_edit),
    path('get_single_project', get_single_project),

]