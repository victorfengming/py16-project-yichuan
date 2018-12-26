from django.conf.urls import url
from . views import IndexViews,LoginViews,CartViews,OrderViews,CenterViews

urlpatterns = [
    # 首页
    url(r'^$',IndexViews.myhome_index,name="myhome_index"),
    # 列表
    url(r'^list/(?P<cid>[0-9]+)',IndexViews.myhome_list,name="myhome_list"),
    # 详情
    url(r'^info/',IndexViews.myhome_info,name="myhome_info"),

    # 登录
    url(r'^login/',LoginViews.myhome_login,name="myhome_login"),
    url(r'^dologin/',LoginViews.myhome_dologin,name="myhome_dologin"),
    url(r'^logout/',LoginViews.myhome_logout,name="myhome_logout"),
    # 注册
    url(r'^register/',LoginViews.myhome_register,name="myhome_register"),
    url(r'^doregister/',LoginViews.myhome_doregister,name="myhome_doregister"),
    # 短信发送
    url(r'^sendMsg/',LoginViews.myhome_sendMsg,name="myhome_sendMsg"),

    # 购物车 增 删 改 查
    url(r'^cart/add/',CartViews.myhome_cart_add,name="myhome_cart_add"),
    url(r'^cart/index/',CartViews.myhome_cart_index,name="myhome_cart_index"),
    url(r'^cart/del/',CartViews.myhome_cart_del,name="myhome_cart_del"),
    url(r'^cart/clear/',CartViews.myhome_cart_clear,name="myhome_cart_clear"),
    url(r'^cart/edit/',CartViews.myhome_cart_edit,name="myhome_cart_edit"),

    # 订单  确认订单,提交订单,订单支付
    url(r'^order/confirm/',OrderViews.myhome_order_confirm,name="myhome_order_confirm"),
    url(r'^order/create/',OrderViews.myhome_order_create,name="myhome_order_create"),
    url(r'^order/pay/',OrderViews.myhome_order_pay,name="myhome_order_pay"),

    # 个人中心  我的订单 个人信息 地址管理
    url(r'^center/order/',CenterViews.myhome_center_order,name="myhome_center_order"),

]
