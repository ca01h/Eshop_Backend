# -*- coding:utf-8 -*-
__author__ = 'cao.yh'
__date__ = '2018/3/29 下午4:40'

# from rest_framework import serializers
# from .models import Goods, GoodsCategory
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"
#
#
# class GoodsSerializer(serializers.ModelSerializer):
#     # name = serializers.CharField(required=True, max_length=100)
#     # click_nums = serializers.IntegerField(default=0)
#     # goods_front_image = serializers.ImageField()
#     #
#     # def create(self, validated_data):
#     #     return Goods.objects.create(**validated_data)
#     class Meta:
#         category = CategorySerializer()
#         model = Goods
#         fields = "__all__"
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类别序列化
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    # 这里的sub_cat 是因为我们在自身的继承关系中将这种关系进行了命名
    # 因为我们此时通过一类拿到的二类有很多，所以必须加上many = True的参数
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )


class GoodsSerializer(serializers.ModelSerializer):
    # 实例化CategorySerializer
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"
