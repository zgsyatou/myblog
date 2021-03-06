from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nickname = models.CharField(max_length= 16, verbose_name= '昵称')

    def __str__(self):
        return '<Profile %s for %s>' % (self.nickname, self.user.username)
# 动态绑定nickname
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else: 
        return ''

# 判断用户是否有昵称
def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

# 判断用户的用户名或者昵称
def has_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else: 
        return self.username

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.has_nickname_or_username = has_nickname_or_username