
## AliPay支付
>支付宝沙箱环境
>内网穿透
>好处,不需要公司企业信息,不需要购买服务器域名..
>支付文档 https://docs.open.alipay.com/270/105898/


### 内网穿透 (ngrok,花生壳)
>内网穿透的实现(建议在windows下安装)

1,到花生壳官网下载一个应用

2,点击开启内网穿透,付费

3,配置内网环境 地址,端口
    http80
    内网环境地址 配置你django服务器所在的地址  192.168.254.128
    内网端口配置为 8000


### 支付宝沙箱环境

1,登录蚂蚁金服开放平台
https://open.alipay.com

2,创建沙箱环境

3,配置秘钥  应用公钥,,应用私钥,,支付宝公钥
    秘钥生成文档: https://docs.open.alipay.com/291/105971

    1,到上面的文档中下载 秘钥工具

    2,解压

    3,生成秘钥和公钥

    4,把公钥配置到 沙箱环境中

4,安装官方SDK
>支付宝官方在2018年5月23日，发布了一个Python版的SDK（公测版）。
>我们可以通过“pip”命令进行安装。
```shell
#安装加密依赖包
pip install pycrypto

#安装alipay-sdk-python。
pip install alipay-sdk-python
```


5,在配置文件中进行 相关设置 settings.py
```python
# 支付宝配置文件

# APPID
# 沙箱APPID，生产环境须更改为应用APPID。
ALIPAY_APPID = "2016092200571332" 

# 网关
# 沙箱网关，生产环境须更改为正式网关。
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do" 
# 正式网关，开发环境勿使用。
# ALIPAY_URL = "https://openapi.alipay.com/gateway.do" 

# 回调通知地址
# 如果只可以内网访问开发服务器
ALIPAY_NOTIFY_URL = "http://127.0.0.1:8000/order/pay_result/" 
# 如果生产环境或外网可以访问开发服务器
# ALIPAY_NOTIFY_URL = "http://1.203.45.678:8000/order/pay_result/" 

# 支付后的跳转地址
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/order/pay_success/'

# 应用私钥
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'keys/app_private_key.txt')
# 支付宝公钥
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'keys/alipay_public_key.txt')
```


6,在项目中配置 keys应用  私钥和支付宝公钥 放进来
    1,在项目中 创建 keys 目录 里面放入 秘钥文件

    2,创建 app_private_key.txt 放入秘钥,加开始和结束的标记
        -----BEGIN RSA PRIVATE KEY-----
        .....
        -----END RSA PRIVATE KEY-----
    3,创建 alipay_public_key.txt 放入秘钥,加开始和结束的标记
        -----BEGIN PUBLIC KEY-----
        ....
        -----END PUBLIC KEY-----


7,根据回调地址的配置,去配置响应的路由和视图函数
    # 支付的回调地址 order/pay_result/
    url(r'^order/pay_result/',OrderViews.myhome_pay_result,name="myhome_pay_result"),
    # 支付宝回调地址
    def myhome_pay_result(request):
        pass

8.配置第三方包 utils

9.在视图函数中 封装一个方法 去实例化alipay对象
    from buydemo import settings
    from utils.pay import AliPay
        
    # AliPay 对象实例化
    def Get_AliPay_Object():
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,# APPID （沙箱应用）
            app_notify_url=settings.ALIPAY_NOTIFY_URL, # 回调通知地址
            return_url=settings.ALIPAY_RETURN_URL,# 支付完成后的跳转地址
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH, # 应用私钥
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
            debug=True,  # 默认False,
        )
        return alipay


10.生成支付的url,重定向到支付页面
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


11,验证回调,成功后修改订单状态


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

