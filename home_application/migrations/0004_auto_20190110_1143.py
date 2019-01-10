# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_remove_wy_records_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wy_records',
            name='creator',
            field=models.CharField(max_length=100, null=True, verbose_name='\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='wy_records',
            name='job_id',
            field=models.CharField(max_length=100, null=True, verbose_name='\u7528\u6237'),
        ),
    ]
