# -*- coding:utf-8 -*-
from utils.alipay import AliPay

__author__ = 'cao.yh'
__date__ = '2018/4/20 上午9:40'
from rest_framework import serializers
import time

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer
from Eshop.settings import private_key_path, ali_pub_key_path


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods_num = serializers.IntegerField(required=True, min_value=1,
                                         error_messages={
                                             'min_value': '商品数量不能小于0',
                                             'required': '请选择购买数量',
                                         })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        """
        记录存在则新增，否则创建
        :param validated_data:
        :return: shoppingcart
        """
        # 在serializer中从self.context['request']取出user
        # 在view中从self.request.user取出user
        user = self.context['request'].user
        goods_num = validated_data['goods_num']
        goods = validated_data['goods']

        shoppingcart = ShoppingCart.objects.filter(user=user, goods=goods)
        if shoppingcart:
            shoppingcart = shoppingcart[0]
            shoppingcart.goods_num += goods_num
            shoppingcart.save()
        else:
            shoppingcart = ShoppingCart.objects.create(**validated_data)

        return shoppingcart

    def update(self, instance, validated_data):
        """
        修改商品数量
        :param instance:
        :param validated_data:
        :return: instance
        """
        instance.goods_num = validated_data['goods_num']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016091500519386",
            app_notify_url="http://122.152.225.37:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://122.152.225.37:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        from random import Random
        random_ins = Random()
        order_sn = '{time_str}{user_id}{random_str}'.format(time_str=time.strftime('%Y%M%D%H%M%S'),
                                                            user_id=self.context['request'].user,
                                                            random_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
        goods = GoodsSerializer(many=False)

        class Meta:
            model = OrderGoods
            fields = "__all__"


class OrderDetailSerializer(serializers.Serializer):
    goods = GoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'
