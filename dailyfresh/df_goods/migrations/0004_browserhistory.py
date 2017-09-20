# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db_user', '0002_address'),
        ('df_goods', '0003_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowserHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('passport', models.ForeignKey(verbose_name='账户', to='db_user.Passport')),
            ],
            options={
                'db_table': 's_browse_history',
            },
        ),
    ]
