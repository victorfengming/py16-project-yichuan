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
