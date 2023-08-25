from django.db.models import Model
from django.shortcuts import render
from django.http import JsonResponse
from message.models import Message
from user.models import User


# Create your views here.
def read_allmessage(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    for message in Message.objects.filter(user=user):
        message.is_read = True
        message.save()
    result = {'result': 0, 'message': '所有消息都为已读'}
    return JsonResponse(result)


def delete_message(request):
    delete_id = request.POST.get('id')
    try:
        message = Message.objects.get(id=delete_id)
        message.delete()
        result = {'result': 0, 'message': '删除消息成功'}
        return JsonResponse(result)
    except Model.DoesNotExist:
        result = {'result': 1, 'message': '消息不存在'}
        return JsonResponse(result)


def delete_allmessage(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    Message.objects.filter(user=user, is_read=True).delete()
    result = {'result': 0, 'message': '所有已读消息已被删除'}
    return JsonResponse(result)
