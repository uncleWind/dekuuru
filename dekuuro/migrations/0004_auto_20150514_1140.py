# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dekuuro', '0003_auto_20150514_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardimage',
            name='image',
        ),
        migrations.DeleteModel(
            name='BoardImage',
        ),
    ]
