# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Goods, GoodsCategory
from goods.serializers import GoodsSerializer, CategorySerializer
from filters import GoodsFilter


# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    """
    配置分页规则
    """
    page_size = 12
    page__size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     """
#     商品列表页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品列表页，分页、搜索、过滤、排序

    retrieve:
        商品详情页
    """


    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #     return Response(goods_serializer.data)

    # 由于商品都是从后台添加的，不是通过用户从前端增加的，所以商品列表页用不到post
    # def post(self, request, format=None):
    #     serilizer = GoodsSeriliazer(data=request.data)
    #     if serilizer.is_valid():
    #         serilizer.save()
    #         return Response(serilizer.data, status=status.HTTP_201_CREATED)
    #     return Response(serilizer.data, status=status.HTTP_400_BAD_REQUEST)

    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination

    queryset = Goods.objects.all()

    # def get_queryset(self):
    #     min_price = self.request.query_params.get("min_price", 0)
    #     if min_price:
    #         self.queryset = Goods.objects.filter(shop_price__gt=int(min_price)).order_by('-add_time')
    #     return self.queryset

    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter, OrderingFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 定义需要过滤的字段
    # filter_fields = ('name', 'shop_price')

    # 指定过滤集合类
    filter_class = GoodsFilter

    # 设置搜索
    # ^ Starts-with search.
    # = Exact matches.
    # @ Full-text search. (Currently only supported Django's MySQL backend.)
    # $ Regex search.
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 设置排序
    ordering_fields = ('sold_num', 'add_time')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据

    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
