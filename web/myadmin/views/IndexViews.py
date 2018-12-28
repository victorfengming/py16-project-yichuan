from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import permission_required

def index(request):
    return render(request,'myadmin/index.html')

# 权限管理 管理员列表
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_index(request):
    # 获取当前所有的管理员
    data = User.objects.all()
    # 分配数据
    context = {'userdata':data}
    # 加载模板
    return render(request,'myadmin/auth/userindex.html',context)

# 权限管理 管理员添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_add(request):
    # 获取当前已经创建的所有 组
    gs = Group.objects.all()
    # 分配数据
    context = {'grouplist':gs}
    # 加载模板
    return render(request,'myadmin/auth/useradd.html',context)

# 权限管理 执行管理员添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_insert(request):
    # 接受表单数据,
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    data.pop('gs')
    # 判断是否为超级管理员
    if data['is_superuser'] == "1":
        data['is_superuser'] = True
        # 创建超级管理员
        ob = User.objects.create_superuser(**data)
    else:
        # 创建普通管理员
        ob = User.objects.create_user(**data)

    # 判断是否给当前用户分配了组
    gs = request.POST.getlist('gs')
    if gs:
        # 给当前管理员设置组
        ob.groups.set(gs)
        ob.save()

    return HttpResponse('<script>alert("创建成功");location.href="/myadmin/auth/user/index/"</script>')

# 权限管理 权限组列表
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_index(request):
    # 获取所有的组
    groupdata = Group.objects.all()
    # 分配数据
    context = {'groupdata':groupdata}
    # 加载模板
    return render(request,'myadmin/auth/groupindex.html',context)
    
# 权限管理 权限组添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_add(request):
    # 读取所有权限信息
    # Permission.objects.all()
    # 读取所有权限信息,并排除以Can开头的系统默认生成权限
    perms = Permission.objects.exclude(name__istartswith='Can')
    # 分配数据
    context = {'perms':perms}
    # 加载模板
    return render(request,'myadmin/auth/groupadd.html',context)

# 权限管理 执行权限组添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_insert(request):
    # 接收组名
    name = request.POST.get('name')

    # 创建组
    g = Group(name=name)
    g.save()

    # 给组设置权限
    prms  = request.POST.getlist('prms',None)
    # 判断是否需要给组添加权限
    if prms:
        # 给组分配权限
        g.permissions.set(prms)
        g.save()

    return HttpResponse('<script>alert("组创建成功");location.href="/myadmin/auth/group/index/"</script>')


# 登录页
def myadmin_login(request):
    
    # 加载页面
    return render(request,'myadmin/login.html')

# 处理登录
def myadmin_dologin(request):
    # 检测验证码是否正确
    if request.session.get('verifycode').upper() != request.POST.get('vcode').upper():
        return HttpResponse('<script>alert("验证码错误");location.href="/myadmin/login/"</script>')
    
    # 检测用户和密码
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # 成功,把用户信息记录在session中
        request.session['AdminUser'] = {'username':user.username,'uid':user.id}
        return HttpResponse('<script>alert("欢迎登录");location.href="/myadmin/"</script>')

    return HttpResponse('<script>alert("账号或密码错误");location.href="/myadmin/login/"</script>')

# 退出登录
def myadmin_logout(request):
    del request.session['AdminUser']
    logout(request)

    return HttpResponse('<script>alert("退出成功");location.href="/myadmin/login/"</script>')


# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
