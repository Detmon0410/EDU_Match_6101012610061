from django.shortcuts import render
from match.models import ChatLog
from django.contrib.auth.models import User
from django import db
from django.db import close_old_connections


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    # function will create coatrooms

    if not ChatLog.objects.filter(chatroom=room_name).exists():
        chat = ChatLog.objects.create(chatroom=room_name)
        chat.save()
    chat = ChatLog.objects.get(chatroom=room_name)
    var_split_log = str(chat.chat_log).split('\n')
    sum_result = ''
    for i in var_split_log:
        # split message from sender to right side
        if request.user.username in i:
            sum_result += '\t\t\t\t\t\t\t\t\t' + i + '\n'
        else:
            # split message receiver to left side
            sum_result += i + '\n'
    close_old_connections()
    db.connection.close()
    return render(request, 'chat/room.html', {
        'room_name': room_name, 'old_message': sum_result
    })
    # filter chatlog to show in text area
