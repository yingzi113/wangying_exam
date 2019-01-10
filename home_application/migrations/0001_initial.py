# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WY_RECORDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_name', models.CharField(max_length=500, null=True, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('job_instance_id', models.IntegerField(null=True, verbose_name='\u4efb\u52a1\u8fd4\u56deID\uff0c\u7528\u4f5c\u8f6e\u8be2\u6807\u5fd7')),
                ('script_name', models.CharField(max_length=500, null=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('bk_biz_id', models.CharField(max_length=100, null=True, verbose_name='\u4e1a\u52a1id')),
                ('bk_biz_name', models.CharField(max_length=100, null=True, verbose_name='\u4e1a\u52a1\u540d\u79f0')),
                ('ips', models.CharField(max_length=500, null=True, verbose_name='IP')),
                ('param_str', models.CharField(max_length=500, null=True, verbose_name='\u53c2\u6570')),
                ('operater_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('status', models.IntegerField(default=1, verbose_name='\u6267\u884c\u72b6\u6001')),
                ('ip_logs', models.TextField(null=True, verbose_name='\u6267\u884c\u7ed3\u679c')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'db_table': 'wy_records',
                'verbose_name': '\u811a\u672c\u6267\u884c\u7ed3\u679c\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='WY_SCRIPY',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u811a\u672c\u540d\u5b57')),
                ('script_type', models.CharField(max_length=100, null=True, verbose_name='\u811a\u672c\u7c7b\u578b')),
                ('script_content', models.TextField(null=True, verbose_name='\u811a\u672c\u5185\u5bb9-base64')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('operator', models.CharField(max_length=100, null=True, verbose_name='\u64cd\u4f5c\u4eba')),
                ('remark', models.CharField(max_length=500, null=True, verbose_name='\u5907\u6ce8')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'db_table': 'wy_script',
                'verbose_name_plural': '\u811a\u672c',
            },
        ),
        migrations.CreateModel(
            name='WY_TASKLIST',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_biz_id', models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1id')),
                ('query_status', models.BooleanField(default=0, verbose_name='\u67e5\u8be2\u72b6\u6001')),
                ('job_instance_id', models.IntegerField(null=True, verbose_name='\u4efb\u52a1\u8fd4\u56deID\uff0c\u7528\u4f5c\u8f6e\u8be2\u6807\u5fd7')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'db_table': 'wy_tasklist',
                'verbose_name': '\u811a\u672c\u6267\u884c\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='WY_USERS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u5b57')),
                ('is_delete', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'db_table': 'wy_user',
                'verbose_name': '\u7528\u6237\u5217\u8868',
            },
        ),
        migrations.AddField(
            model_name='wy_records',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237id', to='home_application.WY_USERS'),
        ),
    ]
