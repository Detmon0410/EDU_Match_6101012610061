from django.contrib import admin

from .models import Human, Subject, WantMatch, Matched, ChatLog, Profile, Student, Tutor, Review, ChatRoomName

admin.site.register(ChatLog)
admin.site.register(Human)
admin.site.register(Tutor)
admin.site.register(WantMatch)
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(ChatRoomName)
