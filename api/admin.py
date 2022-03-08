from django.contrib import admin
from . import models

# Register your models here.

class ChatroomAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Chatroom, ChatroomAdmin)


class MessagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Messages, MessagesAdmin)
