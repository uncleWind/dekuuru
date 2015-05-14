# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dekuuro', '0002_auto_20150514_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='boardID',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='boardusers',
            unique_together=set([('board', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set([('board', 'boardID')]),
        ),
        migrations.AddField(
            model_name='boardimage',
            name='image',
            field=models.ForeignKey(to='dekuuro.Image'),
        ),
    ]
