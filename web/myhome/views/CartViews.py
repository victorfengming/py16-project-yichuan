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


# 购物车商品的删除
def myhome_cart_del(request):
    try:
        # cartid 
        cartid = request.GET.get('cartid')
        # 获取当前购物车商品对象
        ob = Cart.objects.get(id=cartid)
        # 执行删除
        ob.delete()
        return JsonResponse({'code':0,'msg':'删除成功'})
    except:
        pass

    return JsonResponse({'code':1,'msg':'删除失败'})



# 购物车商品数量的修改
def myhome_cart_edit(request):
    try:
        cartid = request.GET.get('cartid')
        num = request.GET.get('num')
        # 根据id获取购物车对象
        ob = Cart.objects.get(id=cartid)
        ob.num = num
        ob.save()
        return JsonResponse({'code':0,'msg':'修改成功'})
    except:
        pass

    return JsonResponse({'code':1,'msg':'修改失败'})


# 购物车商品的清空
def myhome_cart_clear(request):

    return HttpResponse('myhome_cart_clear')


