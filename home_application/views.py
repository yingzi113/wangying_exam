# -*- coding: utf-8 -*-

from common.mymako import render_mako_context


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/task.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def history(request):
    """
    历史记录
    :param request:
    :return:
    """
    return render_mako_context(request, '/home_application/history.html')
