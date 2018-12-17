from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password, check_password
from .. models import Users


# Create your views here.
# 用户模型的管理
# 会员添加表单
def user_add(request):
    return render(request,'myadmin/users/add.html')

# 会员执行添加
def user_insert(request):
    # 接收表单数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 处理密码 加密
    data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

    # 头像上传
    # 接收上传的文件
    myfile = request.FILES.get('pic',None)
    if not myfile:
        # 没有选择头像上传,
        return HttpResponse('<script>alert("没有选择头像上传");history.back(-1);</script>')

    # 处理头像的上传  1.jpg ==> [1,jpg]
    data['pic_url'] = uploads_pic(myfile)
    
    try:
        # 创建模型,添加数据
        ob = Users(**data)
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/myadmin/user/index/";</script>')
    except:
        pass
    return HttpResponse('<script>alert("添加失败");history.back(-1);</script>')


# 会员列表
def user_index(request):
    return HttpResponse('user_index')



# 头像上传的处理代码
def uploads_pic(myfile):
    try:
        import time
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/"+filename,"wb+")
        for chunk in myfile.chunks():# 分块写入文件  
            destination.write(chunk)  
        destination.close()
        return '/static/uploads/'+filename
    except:
        return False
