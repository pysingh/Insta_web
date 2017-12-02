from django.db import models


class InstagramAccounts(models.Model):
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    instagram_password = models.CharField(max_length=128)
    instagram_image = models.CharField(max_length=500)
    instagram_account_status = models.CharField(max_length=128)
    paid_date = models.CharField(max_length=128)


class TargetFunctionalityDB(models.Model):
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    target = models.CharField(default='None',max_length=128)
    target_value = models.CharField(max_length=256)
    following_mediaids = models.CharField(default=0,max_length=256)
    followers_usernameids = models.CharField(default=0,max_length=256)
    pid = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    link_id = models.CharField(default="default", max_length=500)
    pause_follow = models.CharField(default='True', max_length=20)
    pause_like = models.CharField(default='True', max_length=20)

class MessageFunctionalityDB(models.Model):
    message_id = models.CharField(default="default", max_length=500)
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    messages_sent = models.IntegerField(default=0)
    message_pause = models.CharField(default='True', max_length=20)
    pid = models.CharField(default=None,max_length=128)
    status = models.CharField(default='pause', max_length=20)


class AccountDetails(models.Model):
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    following = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    unfollow_count = models.IntegerField(default=0)

class InstagramUnfollowDB(models.Model):
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    cleanup_pause = models.CharField(max_length=20)
    unfollow_count = models.IntegerField(default=0)


'''
class InstagramFollowDatabase(models.Model):
    username = models.CharField(max_length=128)
    instagram_username = models.CharField(max_length=128)
    target = models.CharField(max_length=128)
    target_value = models.CharField(max_length=256)
    pid = models.CharField(max_length=128)

    class Meta:
        app_label = 'Functionalities'

'''