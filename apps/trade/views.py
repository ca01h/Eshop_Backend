# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    update:
        更改商品数量
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin):
    """
    订单管理
    list:
        获取订单列表
    create:
        新增订单
    retrieve:
        获取订单详情
    delete:
        删除订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取用户购物车的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods_num = shop_cart.goods_num
            order_goods.goods = shop_cart.goods
            order_goods.order = order

            order_goods.save()
            shop_cart.delete()
            return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from Eshop.settings import private_key_path, ali_pub_key_path
from rest_framework.response import Response
from utils.alipay import AliPay


class AliPayView(APIView):
    def get(self, request):
        """
        处理支付宝url_return返回
        :param request:
        :return:
        """
        process_dict = {}
        for key, value in request.GET.items():
            process_dict[key] = value

        sign = process_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016091500519386",
            app_notify_url="http://122.152.225.37:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://122.152.225.37:8000/alipay/return/"
        )
        verify_result = alipay.verify(process_dict, sign)

        if verify_result:
            order_sn = process_dict.get('out_trade_no', None)
            trade_no = process_dict.get('trade_no', None)
            trade_status = process_dict.get('trade_status', None)

            exist_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exist_order in exist_orders:
                exist_order.pay_status = trade_status
                exist_order.trade_no = trade_no
                exist_order.pay_time = datetime.now()
                exist_order.save()

            return Response('success')

    def post(self, request):
        """
        处理支付宝notify_return返回
        :param request:
        :return:
        """
        process_dict = {}
        for key, value in request.POST.items():
            process_dict[key] = value


        sign = process_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016091500519386",
            app_notify_url="http://122.152.225.37:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://122.152.225.37:8000/alipay/return/"
        )
        verify_result = alipay.verify(process_dict, sign)

        if verify_result:
            order_sn = process_dict.get('out_trade_no', None)
            trade_no = process_dict.get('trade_no', None)
            trade_status = process_dict.get('trade_status', None)

            exist_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exist_order in exist_orders:
                exist_order.pay_status = trade_status
                exist_order.trade_no = trade_no
                exist_order.pay_time = datetime.now()
                exist_order.save()

            return Response('success')
