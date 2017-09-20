# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('img_url', models.ImageField(verbose_name='图片路径', upload_to='goods/')),
                ('is_def', models.BooleanField(verbose_name='是否默认', default=False)),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
