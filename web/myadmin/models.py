from django.db import models

# Create your models here.


# 定义会员模型
class Users(models.Model):
    nikename = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=77)
    # phone = models.CharField(max_length=11,unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100)
    SEX_CHOICES = (
        (0, '女'),
        (1, '男'),
    )
    sex = models.CharField(max_length=1,null=True,choices=SEX_CHOICES)
    # 0 正常  1禁用  2 删除 ....
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    # 自定义 会员管理 权限
    class Meta:
        permissions = (
            ("show_Users", "查看用户列表权限"),
            ("create_Users", "添加用户信息权限"),
            ("edit_Users", "修改用户信息权限"),
            ("remove_Users", "删除用户信息权限"),
        )



# 商品分类模型
class Cates(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)

    # 自定义 商品分类管理 权限
    class Meta:
        permissions = (
            ("show_Cates", "查看分类列表权限"),
            ("create_Cates", "添加分类信息权限"),
            ("edit_Cates", "修改分类信息权限"),
            ("remove_Cates", "删除分类信息权限"),
        )

# 商品模型
class Goods(models.Model):
    # id 所属分类,商品名,图片,添加时间,销量

    cateid = models.ForeignKey(to="Cates", to_field="id")
    goodsname = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    goodsnum = models.IntegerField()
    pic_url = models.CharField(max_length=255)
    goodsinfo = models.TextField()
    ordernum =  models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    # 0 新品,1热卖,2推荐,3下架
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    # 自定义 商品管理 权限
    class Meta:
        permissions = (
            ("show_Goods", "查看商品列表权限"),
            ("create_Goods", "添加商品信息权限"),
            ("edit_Goods", "修改商品信息权限"),
            ("remove_Goods", "删除商品信息权限"),
        )





# 购物车 模型
class Cart(models.Model):
    # id  用户 uid   商品 goodsid 数量 num
    uid = models.ForeignKey(to="Users", to_field="id")
    goodsid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()


# 订单
class Order(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id")
    username = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    totalprice = models.FloatField()
    # 0 未支付, 1已支付, 2已发货  3已收货  4已评价  5取消 ...
    status = models.IntegerField(default=0)
    # 0 支付宝  1 微信 2 银联  3 其它  4货到付款...
    paytype = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    paytime = models.DateTimeField(null=True)

    # 自定义 订单 权限
    class Meta:
        permissions = (
            ("show_Order", "查看订单列表权限"),
            ("create_Order", "添加订单信息权限"),
            ("edit_Order", "修改订单信息权限"),
            ("remove_Order", "删除订单信息权限"),
        )



# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Order", to_field="id")
    goodsid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()

'''
# 订单
    id订单号 uid用户 收货人,收货地址,收货电话,总价,状态 支付方式 ,下单时间,支付时间
    100011       189     
# 订单详情
    orderid   goodsid   num  price购买时的单价
    100011     12       1
    100011     18       3
'''





