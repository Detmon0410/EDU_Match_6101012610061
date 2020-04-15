
from django.contrib import admin

from .models import Human,Subject,Wantmatch,Matched,Chatlog,Profile,Student,Tutor,Review,Chatroomname

admin.site.register(Chatlog)
admin.site.register(Human)
admin.site.register(Tutor)
admin.site.register(Wantmatch)
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Chatroomname)