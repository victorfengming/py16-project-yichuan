from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse

from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo


# 订单确认页
def myhome_order_confirm(request):

    # 获取选择的购物车id
    cartidstr = request.GET.get('cartids')
    cartids = cartidstr.split(',')
    
    # 把当前选择的购物车数据查询处理
    data = Cart.objects.filter(id__in=cartids)

    # 分配数据
    context = {'cartdata':data}
    
    # 加载模板
    return render(request,'myhome/order/confirm.html',context)



# 订单的创建
def myhome_order_create(request):
    # 接受数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # {'username': '王五', 'address': '北京市', 'cartids': '9,10', 'phone': '13701383017'}
   

    # 创建订单
    ob = Order()
    ob.uid = Users.objects.get(id=request.session.get('VipUser')['uid'])
    ob.username = data['username']
    ob.phone = data['phone']
    ob.address = data['address']
    ob.totalprice = 0
    ob.save()

    # 创建订单详情
    cartdata = Cart.objects.filter(id__in = data['cartids'].split(','))
    totalprice = 0
    for x in cartdata:
        # 创建订单详情
        obinfo = OrderInfo()
        obinfo.orderid = ob
        obinfo.goodsid = x.goodsid
        obinfo.num = x.num
        obinfo.save()
        # 计算总价
        totalprice += x.num*x.goodsid.price
        # 删除购物车中已经下单的商品
        x.delete()

    # 修改订单的总价
    ob.totalprice = totalprice
    ob.save()

    # 重定向到支付页面
    return HttpResponse('<script>alert("订单创建成功,请支付");location.href="/order/pay/?orderid='+str(ob.id)+'"</script>')


# 订单支付
def myhome_order_pay(request):
    # 接收订单号
    orderid = request.GET.get('orderid')
    # 获取订单对象
    order = Order.objects.get(id=orderid)

    # 获取支付对象
    alipay = Get_AliPay_Object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="魅族旗舰官网",  # 商品简单描述
        out_trade_no = orderid,# 用户购买的商品订单号
        total_amount = order.totalprice,  # 交易金额(单位: 元 保留俩位小数)
    )

    # 支付宝网关地址（沙箱应用）
    pay_url = settings.ALIPAY_URL+"?{0}".format(query_params)  
    # 页面重定向到支付页面
    return redirect(pay_url)


# 支付宝回调地址
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def myhome_pay_result(request):
    # 获取对象
    alipay = Get_AliPay_Object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        Order.objects.filter(id=out_trade_no).update(status=1)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        return HttpResponse('<script>alert("支付成功");location.href="/center/order/"</script>')


from web import settings
from utils.pay import AliPay

# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,# APPID （沙箱应用）
        app_notify_url=settings.ALIPAY_NOTIFY_URL, # 回调通知地址
        return_url=settings.ALIPAY_NOTIFY_URL,# 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH, # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay
