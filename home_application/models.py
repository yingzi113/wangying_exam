# -*- coding: utf-8 -*-
from django.db import models
import datetime


class WY_SCRIPY(models.Model):
    name = models.CharField(verbose_name=u'脚本名字', max_length=100,null=True)
    script_type = models.CharField(verbose_name=u'脚本类型', max_length=100, null=True)
    script_content = models.TextField(verbose_name=u"脚本内容-base64", null=True)
    operator = models.CharField(verbose_name=u"操作人", max_length=100, null=True)
    remark = models.CharField(verbose_name=u"备注", max_length=500, null=True)
    is_delete = models.IntegerField(verbose_name=u"是否删除", default=0)

    class Meta:
        verbose_name_plural = u'脚本'
        db_table = 'wy_script'


class WY_USERS(models.Model):

    name = models.CharField(verbose_name=u'名字', max_length=100)
    is_delete = models.IntegerField(verbose_name=u"是否删除", default=0)

    class Meta:
        verbose_name = u'用户列表'
        db_table = 'wy_user'


class WY_TASKLIST(models.Model):

    bk_biz_id = models.CharField(verbose_name='业务id', max_length=100, null=True)
    # 0还未查询 1已经查询
    query_status = models.BooleanField(verbose_name=u'查询状态', default=0)
    job_instance_id = models.IntegerField(verbose_name=u'任务返回ID，用作轮询标志',null=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', default=datetime.datetime.now, null=True)

    class Meta:
        verbose_name = u'脚本执行记录'
        db_table = 'wy_tasklist'



class WY_RECORDS(models.Model):

    record_name = models.CharField(verbose_name=u'任务名称', max_length=500, null=True)
    job_instance_id = models.IntegerField(verbose_name=u'任务返回ID，用作轮询标志', null=True)
    script_name = models.CharField(verbose_name=u'脚本名称', max_length=500, null=True)
    bk_biz_id = models.CharField(verbose_name=u'业务id', max_length=100, null=True)
    bk_biz_name = models.CharField(verbose_name=u'业务名称', max_length=100, null=True)
    creator = models.CharField(verbose_name=u'用户', max_length=100, null=True)
    job_id = models.CharField(verbose_name=u'用户', max_length=100, null=True)
    ips = models.CharField(verbose_name=u'IP',max_length=500, null=True)
    param_str = models.CharField(verbose_name=u'参数', max_length=500, null=True)
    operater_time = models.DateTimeField(verbose_name=u"操作时间", default=datetime.datetime.now)
    #1正在执行 2执行成功 3执行失败
    status = models.IntegerField(verbose_name=u'执行状态', default=1)
    ip_logs = models.TextField(verbose_name=u"执行结果", null=True)
    is_delete = models.IntegerField(verbose_name=u"是否删除", default=0)

    class Meta:
        verbose_name = u'脚本执行结果记录'
        db_table = 'wy_records'

