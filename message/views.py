from django.db.models import Model
from django.shortcuts import render
from django.http import JsonResponse
from message.models import Report
from user.models import User


# Create your views here.
def read_allmessage(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    for message in Report.objects.filter(user=user):
        message.is_read = True
        message.save()
    result = {'result': 0, 'message': '所有消息都为已读'}
    return JsonResponse(result)


def delete_message(request):
    delete_id = request.POST.get('id')
    try:
        message = Report.objects.get(id=delete_id)
        message.delete()
        result = {'result': 0, 'message': '删除消息成功'}
        return JsonResponse(result)
    except Report.DoesNotExist:
        result = {'result': 1, 'message': '消息不存在'}
        return JsonResponse(result)


def delete_allmessage(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    Report.objects.filter(user=user, is_read=True).delete()
    result = {'result': 0, 'message': '所有已读消息已被删除'}
    return JsonResponse(result)


def read_message(request):
    read_id = request.POST.get('id')
    try:
        message = Report.objects.get(id=read_id)
        message.is_read = True
        message.save()
        result = {'result': 0, 'message': '该消息已为已读状态'}
        return JsonResponse(result)
    except Report.DoesNotExist:
        result = {'result': 1, 'message': '该消息不存在'}
        return JsonResponse(result)


def get_messagelist(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    message_list = []
    message_filter_list = Report.objects.filter(user=user).order_by('-created_at')
    if message_filter_list.exists():
        for message in message_filter_list:
            message_list.append(message.to_dic())
        result = {
            'result': 0,
            'message': '获取消息列表成功',
            'list': message_list
        }
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': '消息列表为空'}
        return JsonResponse(result)