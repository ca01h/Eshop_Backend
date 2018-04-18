# -*- coding:utf-8 -*-
from rest_framework.validators import UniqueValidator

__author__ = 'cao.yh'
__date__ = '2018/4/13 下午2:53'
import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from Eshop.settings import REGEX_MOBILE
from .models import VerifyCode


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if VerifyCode.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('手机号码已经注册')

        # 验证手机号码合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码格式错误')

        # 验证码发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile).count():
            raise serializers.ValidationError('请一分钟后再次发送')

        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    # 设置write_only属性可以防止serializer将code字段序列化至前端
    code = serializers.CharField(write_only=True, required=True, allow_blank=False, min_length=4, max_length=4,
                                 label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 })

    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])

    password = serializers.CharField(write_only=True,style={'input': 'password'}, label='密码')

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 获取5分钟之前的时间
            if last_record.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
            # 判断验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
            # 不用将code返回到数据库中，只是做验证
            # return code
        else:
            raise serializers.ValidationError('验证码错误')

    # attrs是每个字段validate之后总的dict
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    # 密码密文处理
    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email","mobile")
