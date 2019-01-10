# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
from django.contrib import admin
from home_application.models import WY_SCRIPY

# from apps.__.models import aaaa
#
# admin.site.register(aaaa)
# ===============================================================================

class WY_SCRIPYAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'script_content')



admin.site.register(WY_SCRIPY,WY_SCRIPYAdmin)

