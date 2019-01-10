# -*- coding: utf-8 -*-

from conf.default import APP_ID, APP_TOKEN
from django.http.request import HttpRequest
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from blueking.component.client import ComponentClient


class ESBApi(object):

    def __init__(self, param):
        if isinstance(param, HttpRequest):
            self.__client = get_client_by_request(param)  # 获取用户登陆态
            self.username = param.user.username
        else:
            self.__client = get_client_by_user(param)  # 获取到用户对象
            self.username = param
        self.__param = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            'bk_username': self.username
        }

    def get_app_by_user(self):
        try:
            param = self.__param
            self.__client.set_bk_api_ver('')
            result = self.__client.cc.get_app_by_user(param)
        except Exception, e:
            result = {'message': e}

        return result


    def search_business(self, page=None):
        if page is None:
            page = {"start": 0, "limit": 20}
        param = self.__param
        fields = ["bk_biz_id", "bk_biz_name"]
        param['fields'] = fields
        param['page'] = page
        self.__client.set_bk_api_ver('v2')
        result = self.__client.cc.search_business(param)

        return result

    def get_set(self, biz_id, page=None):
        try:
            if page is None:
                page = {"start": 0, "limit": 20}
            param = self.__param
            param['bk_biz_id'] = biz_id
            param['page'] = page
            param['condition'] = []
            result = self.__client.cc.search_set(param)
        except Exception, e:
            result = {'message': e}
        return result


    def search_host(self,biz_id,set_id,page=None):
        try:
            if page is None:
                page = {"start": 0, "limit": 20}

            condition = [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": int(biz_id)
                        }
                    ]
                },
                {
                    "bk_obj_id": "set",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_set_id",
                            "operator": "$eq",
                            "value": int(set_id)
                        }
                    ]
                },


            ]
            param = self.__param
            param['bk_biz_id'] = biz_id
            param['page'] = page
            param['condition'] = condition
            result = self.__client.cc.search_host(param)
        except Exception, e:
            result = {'message': e}

        return result

    def get_job_detail(self, bk_job_id, biz_id):

        try:

            param = self.__param
            param['bk_biz_id'] = biz_id
            param['bk_job_id'] = bk_job_id
            result = self.__client.job.get_job_detail(param)
        except Exception, e:
            result = {'message': e}
        return result


    def fast_execute_script(self, bk_biz_id=None, script_id=None, script_content=None, ip_list=None, script_param=None,
                            account=None,script_type=None):
        '''
        执行脚本
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param ip_list:
        :param script_param:
        :param account:
        :return:
        '''
        param = self.__param
        if account is None:
            account = 'root'
        param["bk_biz_id"] = bk_biz_id
        if script_id is not None:
            param["script_id"] = script_id
        if script_content is not None:
            param['script_content'] = script_content
        param["account"] = account
        param["ip_list"] = ip_list
        param["script_type"] = script_type
        if script_param is not None:
            param['script_param'] = script_param
        self.__client.set_bk_api_ver('v2')
        result = self.__client.job.fast_execute_script(param)
        print result, '--------快速执行脚本结果'
        return result

    def execute_job(self, bk_biz_id=None,bk_job_id=None, steps=None, ip_list=None, script_param=None,
                            account=None, script_type=None):
        '''
        执行作业
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param ip_list:
        :param script_param:
        :param account:
        :return:
        '''
        param = self.__param
        if account is None:
            account = 'root'
        param["bk_biz_id"] = bk_biz_id
        param['bk_job_id'] = bk_job_id
        param["account"] = account
        param['steps'] = steps
        # param["ip_list"] = ip_list

        result = self.__client.job.execute_job(param)
        print result, '--------执行作业结果'
        return result

    def get_job_instance_log(self, bk_biz_id=None, job_instance_id=None):
        param = {
            "bk_app_code": self.__param['app_code'],
            "bk_app_secret": self.__param['app_secret'],
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id
        }
        result = self.__client.job.get_job_instance_log(param)
        return result

class ESBComponentApi(object):
    '''
    不需要request参数的esb
    '''

    def __init__(self):

        self.__param = {
            "app_code": APP_ID,
            "app_secret": APP_TOKEN,
            'bk_username': 'admin'
        }
        common_args = {'bk_username': 'admin'}
        self.client = ComponentClient(
            # APP_ID 应用ID
            app_code=APP_ID,
            # APP_TOKEN 应用TOKEN
            app_secret=APP_TOKEN,
            common_args=common_args
        )

    def get_job_list(self, bk_biz_id=None):

        """
        获取作业模版
        :return:
        """

        param = self.__param
        param['bk_biz_id'] = bk_biz_id
        result = self.client.job.get_job_list(param)
        return result

    def fast_execute_script(self, bk_biz_id=None, script_id=None, script_content=None, ip_list=None, script_param=None,
                            account=None, script_type=None):
        '''
        执行脚本
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param ip_list:
        :param script_param:
        :param account:
        :return:
        '''
        param = self.__param
        if account is None:
            account = 'root'
        param["bk_biz_id"] = bk_biz_id
        if script_id is not None:
            param["script_id"] = script_id
        if script_content is not None:
            param['script_content'] = script_content
        param["account"] = account
        param["ip_list"] = ip_list
        param["script_type"] = script_type
        if script_param is not None:
            param['script_param'] = script_param
        result = self.client.job.fast_execute_script(param)
        print result, '--------快速执行脚本结果'
        return result


    def execute_job(self, bk_biz_id=None,bk_job_id=None, steps=None, ip_list=None, script_param=None,
                            account=None, script_type=None):
        '''
        执行作业
        :param bk_biz_id:
        :param script_id:
        :param script_content:
        :param ip_list:
        :param script_param:
        :param account:
        :return:
        '''
        param = self.__param
        if account is None:
            account = 'root'
        param["bk_biz_id"] = bk_biz_id
        param['bk_job_id'] = bk_job_id
        param["account"] = account
        param['steps'] = steps
        # param["ip_list"] = ip_list

        result = self.client.job.execute_job(param)
        print result, '--------执行作业结果'
        return result


    def get_job_instance_log(self, bk_biz_id=None, job_instance_id=None):
        param = {
            "bk_app_code": self.__param['app_code'],
            "bk_app_secret": self.__param['app_secret'],
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id
        }
        result = self.client.job.get_job_instance_log(param)
        return result



