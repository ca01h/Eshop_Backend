# -*- coding: utf-8 -*-
"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin

from Eshop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet


router = DefaultRouter()
# 配置Goods的URL
router.register(r'goods', GoodsListViewSet, base_name='goods')

# good_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

# 配置Category的URL
router.register(r'categories', CategoryViewSet, base_name='categories')

# 配置发送短信验证码的URL
router.register(r'codes', SmsCodeViewSet, base_name='codes')

# 配置用户注册的URL
router.register(r'users', UserViewSet, base_name='users')

# 配置用户收藏的URL
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'ueditor/', include('DjangoUeditor.urls')),

    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^', include(router.urls)),

    # 商品列表页
    # url(r'goods/$', good_list, name="goods_list"),

    # api文档生成
    url(r'docs/', include_docs_urls(title="Eshop")),

    # drf登录配置
    url(r'^api-auth/', include('rest_framework.urls')),

    # drf自带的认证模式
    # url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

]
