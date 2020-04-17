from django.db import models
from django.contrib.auth.models import User


class Human(models.Model):  # user,profiles,subject db
    # receive  and save input from signup page,edit profiles page
    # variable will sent to views.py for display on Profiles page,Match request page
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
    # receive subject in text box on subject page
    # this variable sent to views.py will made user can match when they search same subject
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Wantmatch(models.Model):  # user want match db
    # receive variable when user click match to other profiles
    # this variable sent to views.py for show user on want match page
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Matched(models.Model):  # match user db
    name = models.CharField(max_length=300)
    # receive value when user matched
    # this variable will sent to views.py for this play name of user in student/tutor page

    def __str__(self):
        return self.name


class Tutor(models.Model):  # tutor db
    # receive name user who got match request for other user
    # use for confirm status of match user
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Student(models.Model):  # student db
    # receive name of user who sent match request as student
    # # use for confirm status of match user
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Chatlog(models.Model):  # chat db
    # when chatroom created will receive name of chatroom and then user send message will receive message from chatroom
    # when user join chatroom this variable will sent to chat views.py for display on text area
    chatroom = models.CharField(max_length=300)
    chatlog = models.CharField(max_length=30000000)


class Profile(models.Model):  # user image profile db
    # receive variable when user upload image profile
    # this variable will display on profile picture
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Review(models.Model):  # review db
    # receive variable when user
    post = models.ForeignKey(Human, on_delete=models.CASCADE, related_name='comments', null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    real_name = models.CharField(max_length=300)
    message = models.CharField(max_length=300)
    star = models.IntegerField(null=True)

    class Meta:
        ordering = ['created_on']


class Chatroomname(models.Model):  # chatroom name in match list db
    # receive variable when chatroom created
    # this variable use for lead user join chatroom url
    name = models.CharField(max_length=300, null=True)
