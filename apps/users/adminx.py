# -*- coding:utf-8 -*-
__author__ = 'cao.yh'
__date__ = '2018/3/28 下午6:03'

import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    """
    引入更换主题功能
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """
    页头和页脚
    """
    site_title = "慕学生鲜后台"
    site_footer = "mxshop"
    # 后台的菜单变成下拉式
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)