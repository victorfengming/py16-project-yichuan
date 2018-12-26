from django import template
register = template.Library()

from django.utils.html import format_html
from myadmin.models import Cates
from django.core.urlresolvers import reverse

# 自定义过滤器
# @register.filter
# def py11_upper(val):
#     # print ('val from template:',val)
#     return val.upper()




# 自定义乘法运算标签
@register.simple_tag
def cheng(var1,var2):
    res = float(var1) * float(var2)

    return '%.2f'%res

# 自定义模板导航数据 标签
@register.simple_tag
def showNav():
    # 获取一级分类
    CatesList = Cates.objects.filter(pid=0)
    # print(CatesList)
    s = ''
    for x in CatesList:
        s += '''
        <li class="layout-header-nav-item">
          <a href="{url}" class="layout-header-nav-link">{name}</a>
        </li>
        '''.format(name=x.name,url=reverse('myhome_list',args=(x.id,)))

    return format_html(s)




# 自定义分页标签
@register.simple_tag
def showpage(count,request):
    '''
    count  总页数
    request 请求对象
    '''

    # 接受当前的页码数
    p = int(request.GET.get('page',1))

    # 获取当前请求中所有参数
    data = request.GET.dict()
    args = ''
    for k,v in data.items():
        print(k,v)
        if k != 'page':
            args += '&'+k+'='+v
    # {'types': 'all', 'keywords': 'wu','page':2}
    # &types=all&keywords=wu
    # types=allkeywords=wu
    # &types=all&keywords=wu

    start = p-5
    end = p+4

    # 判断 如果当前页 小于 5
    if p <= 5:
        start = 1
        end = 10
    # 判断 如果当前页 大于 总页数-5
    if p > count-5:
        start = count-9
        end = count
    # 判断 如果总页数 小于 10
    if count < 10:
        start = 1
        end = count

    pagehtml = ''
    # 首页
    pagehtml += '<li><a href="?page=1{args}">首页</a></li>'.format(args=args)
    # 上一页
    if p > 1:
        pagehtml += '<li><a href="?page={p}{args}">上一页</a></li>'.format(p=p-1,args=args)

    for x in range(start,end+1):
        # 判断是否为当前页
        if p == x:
            pagehtml += '<li class="am-active"><a href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)
        else:
            pagehtml += '<li><a href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)
    # 下一页
    if p < count:
        pagehtml += '<li><a href="?page={p}{args}">下一页</a></li>'.format(p=p+1,args=args)
    # 尾页
    pagehtml += '<li><a href="?page={p}{args}">尾页</a></li>'.format(p=count,args=args)

    return format_html(pagehtml)
    # return pagehtml