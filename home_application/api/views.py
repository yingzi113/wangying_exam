# -*- coding: utf-8 -*-

from common.mymako import render_json
from home_application.utils.ESB import ESBApi
from home_application.models import WY_RECORDS,WY_SCRIPY,WY_TASKLIST
from account.decorators import login_exempt
import json
import base64
import time
import datetime
from django.db.models import Q

@login_exempt
def test(request):

    return render_json({
        "result": True,
        "message": 'hello',
        "data": {
            'user': request.user.username,
            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        }
    })




def search_business(request):
    """
    获取业务
    :param request:
    :return:
    """

    response = {}
    try:
        result = ESBApi(request).search_business()
        print result,'======'
        list = []
        if result['result']:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = []
            if len(result['data']['info']) > 0:
                for item in result['data']['info']:
                    dic = {}
                    dic['name'] = item['bk_biz_name']
                    dic['id'] = item['bk_biz_id']
                    list.append(dic)
                response['data'] = list
            else:
                response['result'] = True
                response['code'] = 0
                response['message'] = u'该用户下无业务'
                response['data'] = []
        else:
            response = result

    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = u'获取业务列表失败：%s' % e
        response['data'] = []

    return render_json(response)



def get_set_list(request):
    """
    获取集群列表
    :param request:
    :return:
    """

    response = {}
    bk_biz_id = request.GET.get('bk_biz_id')

    try:
        result = ESBApi(request).get_set(biz_id=bk_biz_id)
        # print result,'====='
        list = []
        if result['code'] == 0:
            for biz_info in result['data']['info']:
                listDic = {}
                listDic['bk_set_id'] = biz_info['bk_set_id']
                listDic['bk_set_name'] = biz_info['bk_set_name']
                listDic['bk_biz_id'] = biz_info['bk_biz_id']
                list.append(listDic)
            response['code'] = 0
            response['result'] = True
            response['data'] = list
            response['message'] = "success"
        else:
            response = result

    except Exception,e:
        response['code'] = 1
        response['result'] = False
        response['data'] = {}
        response['message'] = u'获取失败：%s' % e

    return render_json(response)




def get_host(request):
    """
    获取当前业务下IP列表
    :param request:
    :return:
    """

    response = {}
    bk_biz_id = request.GET.get('bk_biz_id')
    bk_set_id = request.GET.get('bk_set_id')
    print bk_biz_id,bk_set_id

    try:
        result = ESBApi(request).search_host(biz_id=bk_biz_id, set_id=bk_set_id)
        list = []
        if result['code'] == 0:
            for biz_info in result['data']['info']:
                listDic = {}
                listDic['hostname'] = biz_info['host']['bk_host_name']
                listDic['ip'] = biz_info['host']['bk_host_innerip']
                listDic['os_type'] = biz_info['host']['bk_os_type']
                listDic['os_name'] = biz_info['host']['bk_os_name']
                bk_cloud = biz_info['host']['bk_cloud_id']
                listDic['bk_cloud_name'] = bk_cloud[0]['bk_inst_name']
                listDic['bk_cloud_id'] = bk_cloud[0]['bk_inst_id']
                list.append(listDic)
            response['code'] = 0
            response['result'] = True
            response['data'] = list
            response['message'] = "success"

        else:
            response = result

    except Exception, e:
        response['code'] = 1
        response['result'] = False
        response['data'] = {}
        response['message'] = u'获取失败：%s' % e

    return render_json(response)


def get_job_detail(request):
    """
    获取作业详情
    :param request:
    :return:
    """
    response = {}
    bk_biz_id = request.GET.get('bk_biz_id')
    try:
        result = ESBApi(request).get_job_detail(biz_id=bk_biz_id, bk_job_id='1019')
        if result['result']:
            data = result['data']

        response['code'] = 0
        response['result'] = True
        response['data'] = data
        response['message'] = "success"
        print result
    except Exception, e:
        response['code'] = 1
        response['result'] = False
        response['data'] = {}
        response['message'] = u'获取失败：%s' % e

    return render_json(response)


def execute_job(request):
    """
    执行作业
    :param request:
    :return:
    """
    response = {}
    app = request.POST.get('app')
    ip_list = request.POST.get('ip_list')
    ipList = json.loads(ip_list)
    app_item = json.loads(app)
    ips = ''
    for item in ipList:
        ips = ips + item['ip'] + '|'
    ips = ips[0:len(ips) - 1]

    ip_list = []
    for item in ipList:
        ip_list.append({'ip': item['ip'], 'bk_cloud_id': int(item['bk_cloud_id'])})

    try:
        job_detail = ESBApi(request).get_job_detail(biz_id=app_item['id'], bk_job_id='1019')
        if job_detail['result']:
            data = job_detail['data']
            steps = data['steps']
            step = steps[0]
            step['ip_list'] = ip_list
            step['creator'] = request.user.username
            steps[0] = step

        result = ESBApi(request).execute_job(
            bk_biz_id=app_item['id'],
            bk_job_id='1019',
            steps=steps
        )
        print result,'======='

        if result['result']:
            job_instance_id = result['data']['job_instance_id']
            WY_TASKLIST.objects.create(
                bk_biz_id=app_item['id'],
                job_instance_id=job_instance_id,
                query_status=0
            )
            WY_RECORDS.objects.create(
                record_name=result['data']['job_instance_name'],
                job_instance_id=job_instance_id,
                bk_biz_id=app_item['id'],
                bk_biz_name=app_item['name'],
                creator=steps[0]['creator'],
                job_id='1019',
                ips=ips,
                status=1,
                ip_logs=json.dumps(u'执行中')
            )
            response['code'] = 0
            response['result'] = True
            response['message'] = 'success'

        else:
            response = result


    except Exception,e:
        response['code'] = 1
        response['result'] = False
        response['data'] = {}
        response['message'] = u'执行失败：%s' % e


    return render_json(response)



def get_records(request):

    """
    获取任务记录
    :param resquest:
    :return:
    """

    response = {}
    biz_id = request.GET.get('biz_id')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    print biz_id, start_time,end_time

    # start = start = time.strptime(start_time.encode('utf-8').replace('&nbsp;', ' '), '%Y-%m-%d %H:%M:%S')
    # end = time.mktime(time.strptime(json.dumps(end_time), '%Y-%m-%d %H:%M:%S'))
    # print start, end
    try:
        q = Q(is_delete=0)
        if biz_id:
            q.add(Q(bk_biz_id=biz_id), q.AND)
        if start_time:
            start = start_time.encode('utf-8').replace('&nbsp;', ' ')
            q.add(Q(operater_time__gte=start), q.AND)
            print start,'------'
        if end_time:
            end = end_time.encode('utf-8').replace('&nbsp;', ' ')
            q.add(Q(operater_time__lte=end), q.AND)
        records = WY_RECORDS.objects.filter(q).order_by('-operater_time')
        list = []
        if len(records) > 0:
            for item in records:
                dic = {}
                dic['id'] = item.id
                dic['record_name'] = item.record_name
                dic['app_id'] = item.bk_biz_id
                dic['app_name'] = item.bk_biz_name
                dic['ips'] = item.ips
                dic['creator'] = item.creator
                dic['job_id'] = item.job_id
                dic['status'] = item.status
                dic['task_name'] = item.script_name
                dic['detail'] = json.loads(item.ip_logs)
                dic['create_time'] = item.operater_time.strftime('%Y-%m-%d %H:%M:%S')
                ip_log_list = json.loads(item.ip_logs)
                content = ''
                for log_item in ip_log_list:
                    print type(log_item),'log_item'
                    log_content = log_item['log_content']
                    content += '<p>' + log_item['ip'] + '|' + log_content+'\n' + '</p>'


                dic['content'] = content
                print dic

                if item.status == 0:
                    status_message = u'等待'
                elif item.status == 1:
                    status_message = u'正在执行'
                elif item.status == 2:
                    status_message = u'成功'
                else:
                    status_message = u'失败'
                dic['status_message'] = status_message
                list.append(dic)
        response['code'] = 0
        response['result'] = True
        response['data'] = list
        response['message'] = 'success'
    except Exception, e:
        response['code'] = 1
        response['result'] = False
        response['data'] = {}
        response['message'] = u'获取失败：%s' % e
    print response,'-------'

    return render_json(response)