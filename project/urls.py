from django.urls import path

from project.views import *

urlpatterns = [
    path('create_project', create_project),
    path('rename_project', rename_project),
    path('delete_project', delete_project),
    path('get_project', get_project),
    path('create_file', create_file),
    
]