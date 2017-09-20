# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('goods_type_id', models.SmallIntegerField(default=1, verbose_name='商品类型', choices=[(1, '海鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽类蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')])),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_sub_title', models.CharField(max_length=256, verbose_name='商品副标题')),
                ('goods_price', models.DecimalField(max_digits=10, verbose_name='商品价格', decimal_places=2)),
                ('transit_price', models.DecimalField(max_digits=10, verbose_name='商品运费', decimal_places=2)),
                ('goods_unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
                ('goods_stock', models.IntegerField(default=0, verbose_name='商品库存')),
                ('goods_sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('goods_status', models.SmallIntegerField(default=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
    ]
