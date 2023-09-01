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
    path('get_single_project', get_single_project),
    path('doc_at', doc_at),
    path('create_folder', create_folder),
    path('get_doc_in_folder', get_doc_in_folder),
    path('search_project', search_project),
    path('copy_project', copy_project),
    path('delete_folder', delete_folder),
    path('get_invite_doc_link', get_invite_doc_link),
    path('set_guest_editable', set_guest_editable),
    path('get_guest_editable', get_guest_editable),
    path('get_team_id_by_doc_id', get_team_id_by_doc_id),

]