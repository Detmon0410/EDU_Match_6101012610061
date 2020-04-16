from django.db import models
from django.contrib.auth.models import User


class Human(models.Model):  # user,profiles,subject db
    name = models.CharField(max_length=300)
    subject = models.ManyToManyField('Subject')
    wantmatch = models.ManyToManyField('Wantmatch')
    matched = models.ManyToManyField('Matched')
    tutor = models.ManyToManyField('Tutor')
    student = models.ManyToManyField('Student')
    chatroomname = models.ManyToManyField('Chatroomname')

    def __str__(self):
        return self.name


class Subject(models.Model):  # subject db
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Wantmatch(models.Model):  # user want match db
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Matched(models.Model):  # match user db
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Tutor(models.Model):  # tutor db
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Student(models.Model):  # student db
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Chatlog(models.Model):  # chat db
    chatroom = models.CharField(max_length=300)
    chatlog = models.CharField(max_length=30000000)


class Profile(models.Model):  # user image profile db
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Review(models.Model):  # review db
    post = models.ForeignKey(Human, on_delete=models.CASCADE, related_name='comments', null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    realname = models.CharField(max_length=300)
    message = models.CharField(max_length=300)
    star = models.IntegerField(null=True)

    class Meta:
        ordering = ['created_on']


class Chatroomname(models.Model):  # chatroom name in match list db
    name = models.CharField(max_length=300, null=True)
