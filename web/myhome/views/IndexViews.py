from django.shortcuts import render
from django.http import HttpResponse,Http404

from myadmin.models import Cates,Goods

# Create your views here.


# 首页
def myhome_index(request):

    '''
        data = [
            {
                'name':'手机',
                'sub':[
                        {'name':'魅蓝手机','goodslist':[{},{},{}]},
                        {'name':'没煮手机','goodslist':[{},{},{}]}
                    ]
            },
            {
                'name':'智能设备',
                'sub':[
                        {'name':'智能手环','goodslist':[{},{},{}]},
                        {'name':'智能厨房','goodslist':[{},{},{}]}
                    ]
            }
        ]
    '''
    # 先获取一级分类
    data = Cates.objects.filter(pid=0)
    # 在一级分类下 追加一个sub属性,
    for x in data:
        # sub属性里存放的是当前一级分类下的 二级子类
        x.sub = Cates.objects.filter(pid=x.id)


    # 分配数据
    context = {'navdata':data}

    # 加载模板
    return render(request,'myhome/index/index.html',context)

# 列表
def myhome_list(request,cid):
    # 根据cid获取当前分类对象
    ob = Cates.objects.get(id=cid)
    # 判断当前是否为一级类
    if ob.pid == 0:
        # 获取当前一级类的所有子类
        ob.sub = Cates.objects.filter(pid=ob.id)
        # 获取当前二级分类下的所有商品
        goods = []
        for x in ob.sub:
            goods += x.goods_set.all().values()
        # 把当前分类下商品追加到数据中
        ob.goods = goods
        # 分配数据
        context = {'Cateslist':ob}
    else:
        # 获取当前分类的 父级
        pob = Cates.objects.get(id=ob.pid)
        # 获取当前二级分类的 同级分类
        pob.sub = Cates.objects.filter(pid=pob.id)
        for x in pob.sub:
            if x.id == ob.id:
                # 给当前的二级类加一个标识
                x.index = True
                
        # 获取当前类下商品,不要同类的商品
        pob.goods = ob.goods_set.all()
        # 分配数据
        context = {'Cateslist':pob}



    '''
    ob
    {
        'name':'手机',
        'sub':[{'name':'魅族'},{'name':'魅蓝'}],
        'goods':[]
    }
    pob
    {
        'name':'手机',
        'sub':[{'name':'魅族'},{'name':'魅蓝'}],
        'goods':[]

    }
    '''


    # 加载模板
    return render(request,'myhome/index/list.html',context)

# 详情
def myhome_info(request):
    try:
        # 根据商品id获取商品数据
        ob = Goods.objects.get(id=request.GET.get('goodsid'))
        # 分配数据
        context = {'goods':ob}
        # 加载模板
        return render(request,'myhome/index/info.html',context)
    except:
        pass

    raise Http404('您需要的页面找不到了...')
        


