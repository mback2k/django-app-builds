# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name='Number')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('result', models.SmallIntegerField(blank=True, null=True, verbose_name='Result', choices=[(0, 'Success'), (1, 'Warnings'), (2, 'Failure'), (3, 'Skipped'), (4, 'Exception'), (5, 'Retry')])),
                ('simplified_result', models.NullBooleanField(verbose_name='Simplified result')),
                ('start_time', models.DateTimeField(null=True, verbose_name='Start time', blank=True)),
                ('end_time', models.DateTimeField(null=True, verbose_name='End time', blank=True)),
                ('duration', models.IntegerField(null=True, verbose_name='Duration', blank=True)),
                ('properties', models.TextField(verbose_name='Properties')),
                ('data', models.TextField(verbose_name='Data')),
            ],
            options={
                'ordering': ('-start_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='Name')),
                ('link', models.URLField(help_text='JSON API', verbose_name='Link')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision', models.CharField(max_length=40, verbose_name='Revision')),
                ('comments', models.TextField(verbose_name='Comments')),
                ('when', models.DateTimeField(verbose_name='When')),
                ('who', models.CharField(max_length=100, verbose_name='Who')),
            ],
            options={
                'ordering': ('-when',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='change',
            name='project',
            field=models.ForeignKey(related_name=b'changes', to='builds.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='change',
            name='repository',
            field=models.ForeignKey(related_name=b'changes', blank=True, to='builds.Repository', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='change',
            unique_together=set([('project', 'repository', 'revision')]),
        ),
        migrations.AddField(
            model_name='build',
            name='builder',
            field=models.ForeignKey(related_name=b'builds', to='builds.Builder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='build',
            name='changes',
            field=models.ManyToManyField(related_name=b'builds', to='builds.Change'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('builder', 'number')]),
        ),
    ]
