# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_sign', models.CharField(max_length=100, verbose_name='Call Sign')),
                ('crew', models.CharField(blank=True, max_length=20, null=True, verbose_name='Crew')),
                ('badge', models.CharField(blank=True, max_length=20, null=True, verbose_name='Badge')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
        ),
        migrations.AddField(
            model_name='mission',
            name='vehicles',
            field=models.ManyToManyField(to='base.Vehicle'),
        ),
    ]