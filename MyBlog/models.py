from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Friends(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


class Article(models.Model):
    title = models.CharField(max_length=200,null=True)
    text = RichTextField(null=True)
    preview = RichTextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    tags = TaggableManager()
    members = models.ManyToManyField(User,related_name='members', blank=True)
    STATUS = (('Активна', 'Active'),
                ('Выполнена', 'Сompleted'),
                )
    status = models.CharField(max_length=9, choices=STATUS, default='Active')

    def __str__(self):
        return self.title

    def get_user(self):
        return self.user


class Subscriber(models.Model):
    email = models.EmailField('', max_length=100, null=True, blank=True)
