# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('board_tag', models.CharField(unique=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='BoardSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('board', models.ForeignKey(to='dekuuro.Board')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoardUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priviledge_level', models.CharField(max_length=3, choices=[(b'ADM', b'Admin'), (b'MOD', b'Moderator'), (b'UPL', b'Uploader'), (b'STD', b'Standard')])),
                ('board', models.ForeignKey(to='dekuuro.Board')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=500)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('URI', models.FileField(max_length=400, upload_to=b'')),
                ('thumb_URI', models.FileField(max_length=400, upload_to=b'')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(to='dekuuro.Board')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('board', models.ForeignKey(to='dekuuro.Board')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='filtered_tags',
            field=models.ManyToManyField(to='dekuuro.Tag'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(to='dekuuro.Tag'),
        ),
        migrations.AddField(
            model_name='image',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(to='dekuuro.Image'),
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('board', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='boardsubscription',
            unique_together=set([('user', 'board')]),
        ),
    ]
