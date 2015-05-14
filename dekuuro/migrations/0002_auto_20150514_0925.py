# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_thumbs.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dekuuro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='thumb_URI',
        ),
        migrations.AlterField(
            model_name='image',
            name='URI',
            field=django_thumbs.db.models.ImageWithThumbsField(upload_to=b''),
        ),
    ]
