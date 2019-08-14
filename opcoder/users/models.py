from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from datetime import datetime


class UserProfile(AbstractUser):
    link = models.URLField('个人网址', blank=True, help_text='提示：网址必须填写以 http 开头的完整形式')
    nick_name = models.CharField(max_length=20, verbose_name='昵称', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    avatar = ProcessedImageField(
        upload_to='avatar/%Y/%m/%d',
        default='avatar/default.png',
        verbose_name='头像',
        processors=[ResizeToFill(80, 80)]
    )

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username