# -*- coding:utf-8 -*-
__author__ = 'cao.yh'
__date__ = '2018/4/2 上午10:29'

from django_filters import rest_framework as filters
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    # 行为：确定价格区间
    price_min = filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = filters.NumberFilter(name='shop_price', lookup_expr='lte')
    # 行为: 名称中包含某字符，且字符不区分大小写
    name = filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name', 'is_hot']
