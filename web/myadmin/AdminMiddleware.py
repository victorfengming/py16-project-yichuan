from django.shortcuts import render
from django.http import HttpResponse
import re

from django.core.urlresolvers import reverse

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):


        # 后台登录的验证中间件
        # 用户的请求路径# /myadmin/cate/index/
        path = request.path
        # 定义允许访问的路径
        arr = ['/myadmin/login/','/myadmin/dologin/','/myadmin/verifycode/']
        # 检测用户是否访问后台,并且不是进入登录页面
        if re.match('/myadmin/',path) and path not in arr:
            # 检测是否已经登录
            AdminUser = request.session.get('AdminUser',None)
            if not AdminUser:
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/"</script>')


        # 前台登录的验证中间件
        homeurl = [
            reverse('myhome_cart_add'),
            reverse('myhome_cart_index'),
            reverse('myhome_cart_del'),
            reverse('myhome_cart_clear'),
            reverse('myhome_cart_edit'),
            reverse('myhome_order_confirm'),
            reverse('myhome_order_create'),
            reverse('myhome_order_pay'),
            reverse('myhome_center_order'),
        ]
        print(path)
        # 判断 用户是否进入以上需要登录的页面中
        if path in homeurl:
            # 检测当前用户是否登录
            if not request.session.get('VipUser',None):
                # 如果没有登录,则跳转到登录页面
                return HttpResponse('<script>alert("请先登录");location.href="/login/"</script>')


        response = self.get_response(request)
        return response