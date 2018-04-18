# -*- coding:utf-8 -*-
__author__ = 'cao.yh'
__date__ = '2018/4/18 上午10:08'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户
    user = serializers.CharField(read_only=True ,default=serializers.CurrentUserDefault())

    # 这种方法也可以获取当前用户，但是user字段不会序列化到前端
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        model = UserFav

        # 这个validate是写在meta信息中的，是因为它不是作用于某一个字段之上了。
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        # 删除时需要id字段
        fields = ('user', 'goods', 'id')
