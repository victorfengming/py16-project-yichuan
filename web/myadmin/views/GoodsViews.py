from django.shortcuts import render
from django.http import HttpResponse

from . CatesViews import get_cates_all
from . UsersViews import uploads_pic

from .. models import Cates,Goods

# Create your views here.
from django.contrib.auth.decorators import permission_required


# 商品添加 表单
@permission_required('myadmin.create_Goods',raise_exception=True)
def goods_add(request):

    # 获取当前所有的分类数据
    data = get_cates_all()
    # 分配数据
    context = {'catelist':data}

    # 显示一个添加的表单
    return render(request,'myadmin/goods/add.html',context)

@permission_required('myadmin.create_Goods',raise_exception=True)
def goods_insert(request):
    try:
    
        # 接收表单数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 处理 分类对象
        data['cateid'] = Cates.objects.get(id=data['cateid'])
        # 判断是否有图片上传
        myfile = request.FILES.get('pic',None)
        if not myfile:
            return HttpResponse('<script>alert("必须上传商品图片");history.back(-1);</script>')
        # 处理  上传的文件
        data['pic_url'] = uploads_pic(myfile)

        # 执行添加
        ob = Goods(**data)
        ob.save()
        
        return HttpResponse('<script>alert("商品添加成功");location.href="/myadmin/goods/index/";</script>')
    except:
        pass

    return HttpResponse('<script>alert("商品添加失败");history.back(-1);";</script>')


@permission_required('myadmin.show_Goods',raise_exception=True)
def goods_index(request):
    
    # 获取所有的商品对象
    data = Goods.objects.all()

    # 分配数据
    context = {'goodslist':data}

    # 加载模板
    return render(request,'myadmin/goods/index.html',context)
    

