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
            name='Cart',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('goods_count', models.ImageField(default=1, verbose_name='商品数目', upload_to='')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='商品')),
                ('passport', models.ForeignKey(to='db_user.Passport', verbose_name='账户')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
