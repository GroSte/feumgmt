# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FireHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('chief', models.CharField(blank=True, max_length=200, null=True, verbose_name='Chief')),
                ('street', models.CharField(blank=True, max_length=200, null=True, verbose_name='Street')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Location')),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone Number')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='Creation date')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Last update')),
            ],
            options={
                'verbose_name': 'Fire House',
                'verbose_name_plural': 'Fire Houses',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
                ('text', models.TextField(verbose_name='Text')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='Expiration Date')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='Creation date')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Last update')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'permissions': (('view_message', 'Can view messages'),),
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('chief', models.CharField(blank=True, max_length=200, null=True, verbose_name='Chief')),
                ('street', models.CharField(blank=True, max_length=200, null=True, verbose_name='Street')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Location')),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone Number')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='Creation date')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Last update')),
            ],
            options={
                'verbose_name': 'Municipality',
                'verbose_name_plural': 'Municipalities',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, max_length=20, null=True, verbose_name='Grade')),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone Number')),
                ('mobile_phone_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='Mobile Phone Number')),
                ('birth_date', models.DateField(blank=True, max_length=45, null=True, verbose_name='Birth Date')),
                ('admittance_date', models.DateField(blank=True, null=True, verbose_name='Admittance Date')),
                ('breathing_protection_carrier', models.BooleanField(default=False, verbose_name='Breathing Protection Carrier')),
                ('next_medical_examination_date', models.DateField(blank=True, null=True, verbose_name='Next Medical Examination Date')),
                ('next_breathing_protection_training_date', models.DateField(blank=True, null=True, verbose_name='Next Breathing Protection Training Date')),
                ('online', models.BooleanField(default=False, verbose_name='Online')),
                ('online_date', models.DateTimeField(blank=True, null=True, verbose_name='Online date')),
                ('online_ip', models.CharField(blank=True, max_length=15, null=True, verbose_name='Online IP')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='Creation date')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Last update')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user',
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'permissions': (('view_breathingprotectioncarrier', 'Can view breathing protection carriers'), ('change_breathingprotectioncarrier', 'Can change breathing protection carrier')),
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_sign', models.CharField(max_length=100, verbose_name='Call Sign')),
                ('crew', models.CharField(blank=True, max_length=20, null=True, verbose_name='Crew')),
                ('number_plate', models.CharField(blank=True, max_length=20, null=True, verbose_name='Number Plate')),
                ('creation_date', models.DateTimeField(blank=True, null=True, verbose_name='Creation date')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Last update')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.UserProfile', verbose_name='Editor')),
                ('fire_house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.FireHouse', verbose_name='Fire House')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
        ),
        migrations.AddField(
            model_name='municipality',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='municipality_editor', to='base.UserProfile', verbose_name='Editor'),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to='base.UserProfile', verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='message',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_editor', to='base.UserProfile', verbose_name='Editor'),
        ),
        migrations.AddField(
            model_name='firehouse',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fire_house_editor', to='base.UserProfile', verbose_name='Editor'),
        ),
        migrations.AddField(
            model_name='firehouse',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Municipality', verbose_name='Municipality'),
        ),
    ]
