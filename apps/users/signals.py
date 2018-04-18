# -*- coding:utf-8 -*-
__author__ = 'cao.yh'
__date__ = '2018/4/14 下午1:31'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()