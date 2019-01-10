# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_remove_wy_scripy_create_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wy_records',
            name='user',
        ),
    ]
