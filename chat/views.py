from django.shortcuts import render
from match.models import Chatlog
from django.contrib.auth.models import User
from django import db
from django.db import close_old_connections


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):  # function will create coatrooms

    if not Chatlog.objects.filter(chatroom=room_name).exists():
        chat = Chatlog.objects.create(chatroom=room_name)
        chat.save()
    chat = Chatlog.objects.get(chatroom=room_name)
    splited_log = str(chat.chatlog).split('\n')
    sum = ''
    for i in splited_log:
        if request.user.username in i:
            sum += '\t\t\t\t\t\t\t\t\t' + i + '\n'
        else:
            sum += i + '\n'
    close_old_connections()
    db.connection.close()
    return render(request, 'chat/room.html', {
        'room_name': room_name, 'old_message': sum
    })
    # filter chatlog to show in text area
