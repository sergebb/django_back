from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chatroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='UserRooms', related_name='joinedrooms')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'chatroom'
        verbose_name_plural = 'chatrooms'
        ordering = ('name',)


class UserRooms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)


class Messages(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, null=False)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return self.user.username + ': ' + self.text

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('date', )
