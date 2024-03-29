# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-28 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0006_auto_20181228_0913'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cates',
            options={'permissions': (('show_Cates', '查看分类列表权限'), ('create_Cates', '添加分类信息权限'), ('edit_Cates', '修改分类信息权限'), ('remove_Cates', '删除分类信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('show_Goods', '查看商品列表权限'), ('create_Goods', '添加商品信息权限'), ('edit_Goods', '修改商品信息权限'), ('remove_Goods', '删除商品信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': (('show_Order', '查看订单列表权限'), ('create_Order', '添加订单信息权限'), ('edit_Order', '修改订单信息权限'), ('remove_Order', '删除订单信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'permissions': (('show_Users', '查看用户列表权限'), ('create_Users', '添加用户信息权限'), ('edit_Users', '修改用户信息权限'), ('remove_Users', '删除用户信息权限'))},
        ),
    ]
