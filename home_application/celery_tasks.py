# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from home_application.utils.ESB import ESBComponentApi,ESBApi
from home_application.models import WY_RECORDS,WY_SCRIPY,WY_TASKLIST,WY_USERS
import json
from common.log import logger


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))




@periodic_task(run_every=5)
def getting_job_result():

    """
    查询脚本执行结果
    作业状态码: 1.未执行; 2.正在执行; 3.执行成功; 4.执行失败; 5.跳过; 6.忽略错误; 7.等待用户; 8.手动结束; 9.状态异常; 10.步骤强制终止中; 11.步骤强制终止成功; 12.步骤强制终止失败

    :return:
    """

    task_list = WY_TASKLIST.objects.all()
    if len(task_list) > 0:
        for task in task_list:
            instance_id = task.job_instance_id
            bk_biz_id = task.bk_biz_id
            get_exec_log(task=task, biz_id=bk_biz_id, instance_id=instance_id)




@task
def get_exec_log(task, biz_id, instance_id):
    """
    获取执行结果
    :param task:
    :param biz_id:
    :param job_instance_id:
    :return:
    """
    job_exec_log = ESBComponentApi().get_job_instance_log(
        bk_biz_id=biz_id,
        job_instance_id=instance_id
    )
    print instance_id,job_exec_log
    print json.dumps(job_exec_log),'job_exec_log'
    if job_exec_log['result']:
        if job_exec_log['data'][0]['status'] == 2:
            # 正在执行
            modify_data(data={},task=task, status=1, instance_id=instance_id)
            task.query_status = 1
            task.save()
        elif job_exec_log['data'][0]['status'] == 3:
            # 执行成功
            ip_logs = json.dumps(job_exec_log['data'][0]['step_results'][0]['ip_logs'])
            print ip_logs,'ip_logs'
            modify_data(data=ip_logs, task=task, status=2, instance_id=instance_id)
            task.delete()
        else:
            # 执行失败
            ip_logs = json.dumps(job_exec_log['data'][0]['step_results'][0]['ip_logs'])
            modify_data(data=ip_logs,task=task, status=3, instance_id=instance_id)
            task.delete()



def modify_data(data,task,status,instance_id):

    """
    修改数据
    :param task:
    :param biz_id:
    :param instance_id:
    :return:
    """
    records = WY_RECORDS.objects.filter(job_instance_id=instance_id)
    if len(records) > 0:
        item = records[0]
        if status == 1:
            item.status = 1
            item.save()
        elif status == 2:
            item.status = 2
            item.ip_logs = data
            item.save()
        else:
            item.status = 3
            item.ip_logs = data
            item.save()







