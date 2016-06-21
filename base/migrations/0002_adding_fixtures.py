# -*- coding: utf-8 -*-
from django.db import migrations
from base.utils import LoadDataWithModelState

data_loader = LoadDataWithModelState('base_data.json')


# create a new dump:
# python manage.py dumpdata auth base contenttypes > base/fixtures/base_data.json
class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=data_loader.load,
            reverse_code=lambda: True,
        ),
    ]
