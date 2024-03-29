from django.conf.urls import url
from . views import IndexViews,UsersViews,CatesViews,GoodsViews

urlpatterns = [
    url(r'^$',IndexViews.index,name="myadmin_index"),

    # 权限管理
    # 管理员管理
    url(r'^auth/user/index/$',IndexViews.myadmin_authuser_index,name="myadmin_authuser_index"),
    url(r'^auth/user/add/$',IndexViews.myadmin_authuser_add,name="myadmin_authuser_add"),
    url(r'^auth/user/insert/$',IndexViews.myadmin_authuser_insert,name="myadmin_authuser_insert"),
    
    # 权限组管理
    url(r'^auth/group/index/$',IndexViews.myadmin_authgroup_index,name="myadmin_authgroup_index"),
    url(r'^auth/group/add/$',IndexViews.myadmin_authgroup_add,name="myadmin_authgroup_add"),
    url(r'^auth/group/insert/$',IndexViews.myadmin_authgroup_insert,name="myadmin_authgroup_insert"),
    

    # 登录页
    url(r'^login/$',IndexViews.myadmin_login,name="myadmin_login"),
    url(r'^dologin/$',IndexViews.myadmin_dologin,name="myadmin_dologin"),
    url(r'^logout/$',IndexViews.myadmin_logout,name="myadmin_logout"),
    url(r'^verifycode/$',IndexViews.verifycode,name="myadmin_vcode"),

    # 会员管理
    url(r'^user/add/$',UsersViews.user_add,name="myadmin_user_add"),
    url(r'^user/insert/$',UsersViews.user_insert,name="myadmin_user_insert"),
    url(r'^user/index/$',UsersViews.user_index,name="myadmin_user_index"),
    url(r'^user/edit/$',UsersViews.user_edit,name="myadmin_user_edit"),
    url(r'^user/setstatus/$',UsersViews.user_set_status,name="myadmin_user_set_status"),

    # 分类管理
    url(r'^cate/add/$',CatesViews.cate_add,name="myadmin_cate_add"),
    url(r'^cate/index/$',CatesViews.cate_index,name="myadmin_cate_index"),
    url(r'^cate/del/$',CatesViews.cate_del,name="myadmin_cate_del"),
    url(r'^cate/edit/$',CatesViews.cate_edit,name="myadmin_cate_edit"),

    # 商品管理
    url(r'^goods/add/$',GoodsViews.goods_add,name="myadmin_goods_add"),
    url(r'^goods/insert/$',GoodsViews.goods_insert,name="myadmin_goods_insert"),
    url(r'^goods/index/$',GoodsViews.goods_index,name="myadmin_goods_index"),
]
