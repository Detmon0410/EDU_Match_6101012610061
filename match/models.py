from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Human(models.Model):

    name = models.CharField(max_length=300)
    subject = models.ManyToManyField('Subject')
    wantmatch = models.ManyToManyField('Wantmatch')
    matched = models.ManyToManyField('Matched')
    tutor = models.ManyToManyField('Tutor')
    student = models.ManyToManyField('Student')
    chatroomname = models.ManyToManyField('Chatroomname')
    def __str__(self):
        return self.name


class Subject(models.Model):

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Wantmatch(models.Model):

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
class Matched(models.Model):

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
class Tutor(models.Model):

    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name
class Student(models.Model):

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class chatlog(models.Model):
    chatroom=models.CharField(max_length=300)
    chatlo=models.CharField(max_length=30000000)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
class Review(models.Model):
    post = models.ForeignKey(Human, on_delete=models.CASCADE, related_name='comments',null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    realname=models.CharField(max_length=300)
    message = models.CharField(max_length=300)
    star =models.IntegerField(null=True)

    class Meta:
        ordering = ['created_on']


class Chatroomname(models.Model):
    name= models.CharField(max_length=300,null=True)