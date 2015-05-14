# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dekuuro.models
import django_thumbs.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dekuuro', '0004_auto_20150514_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='URI',
            field=django_thumbs.db.models.ImageWithThumbsField(upload_to=dekuuro.models.imageUpload),
        ),
    ]
