# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0004_browserhistory'),
        ('db_user', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('order_id', models.CharField(primary_key=True, max_length=64, verbose_name='订单id', serialize=False)),
                ('total_count', models.IntegerField(verbose_name='商品总数', default=1)),
                ('total_price', models.DecimalField(verbose_name='商品总额', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='订单运费', decimal_places=2, max_digits=10)),
                ('pay_method', models.IntegerField(verbose_name='支付方式', default=1)),
                ('order_status', models.IntegerField(verbose_name='订单状态', default=1)),
                ('addr', models.ForeignKey(verbose_name='收件地址', to='db_user.Address')),
                ('passport', models.ForeignKey(verbose_name='用户', to='db_user.Passport')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('goods_count', models.IntegerField(verbose_name='商品数目', default=1)),
                ('goods_price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('order', models.ForeignKey(verbose_name='基本订单', to='df_order.OrderBasic')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
