from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse

from myadmin.models import Cates,Goods,Cart,Users

# Create your views here.
# 购物车的添加
def myhome_cart_add(request):
    try:
        # 执行购物车的商品添加
        data = request.GET.dict()
        data['goodsid'] = Goods.objects.get(id=data['goodsid'])
        data['uid'] = Users.objects.get(id=request.session.get('VipUser')['uid'])
        # 先检测当前的商品是否已经在当前用户的购物车中
        ob = Cart.objects.filter(uid=data['uid']).filter(goodsid=data['goodsid'])
        if ob.count():
            # 存在 获取当前购物车对象
            cart = Cart.objects.get(id=ob[0].id)
            cart.num += int(data['num'])
            cart.save()
        else:
            # 不存在
            # 存入 cart模型中
            ob = Cart(**data)
            ob.save()
        return JsonResponse({'code':0,'msg':'加入购物车成功'})
    except:
        pass
    return JsonResponse({'code':1,'msg':'加入购物车失败'})


# 购物车的列表
def myhome_cart_index(request):

    # 获取当前用户的购物车数据
    VipUser = request.session.get('VipUser')
    data = Cart.objects.filter(uid=VipUser['uid'])
    # 分配数据
    context = {'cartdata':data}
    # 加载模板
    return render(request,'myhome/cart/index.html',context)

def myhome_cart_del(request):

    return HttpResponse('myhome_cart_del')

def myhome_cart_clear(request):

    return HttpResponse('myhome_cart_clear')

def myhome_cart_edit(request):

    return HttpResponse('myhome_cart_edit')


