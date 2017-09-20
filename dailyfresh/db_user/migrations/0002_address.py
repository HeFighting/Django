# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('recipient_name', models.CharField(max_length=20, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='收件地址')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮编')),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
                ('passport', models.ForeignKey(verbose_name='所属账户', to='db_user.Passport')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
