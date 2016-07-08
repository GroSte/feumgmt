# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os

from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from base.importer import Importer
from base.models import UserProfile
from event.models import Training


class TrainingImporter(Importer):
    mapping = {
        'date': 'DATUM',
        'subject': 'THEMA',
        'responsibles': 'VERANTWORTLICHER',
        'note': 'SONSTIGES',
    }

    def get_trainings_from_csv_file(self, file_name='config/training.csv'):
        current_mapping = {}
        base_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(os.path.join(base_path, os.pardir))
        path = os.path.join(path, file_name)
        rows = []
        with open(path, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=b';', quotechar=b'"')
            for row in reader:
                if len(current_mapping) == 0:
                    current_mapping = self.get_current_mapping(row)
                    continue
                rows.append(row)

        trainings = []
        for row in rows:
            training = {}
            for field, index in current_mapping.iteritems():
                training[field] = row[index - 1]
            trainings.append(training)

        for training in trainings:
            training['date'] = datetime.fromtimestamp(int(training['date']))
            training['responsibles'] = self.get_responsibles(training['responsibles'])
        return trainings

    def get_responsibles(self, raw_string):
        responsibles = []
        raw_string = unicode(raw_string, 'utf-8')
        raw_names = raw_string.split(',')
        for raw_name in raw_names:
            raw_name = raw_name.strip()
            name_parts = raw_name.split(' ')
            if len(name_parts) > 1:
                # try to get users like 'Meier, A.'
                last_name = name_parts[0]
                first_name = name_parts[1][:1]
                users = User.objects.filter(last_name=last_name, first_name__startswith=first_name)
            else:
                # try to get users like 'Meier'
                users = User.objects.filter(last_name=raw_name)

            try:
                user = users.first()
                user_profile = UserProfile.objects.get(user_id=user.id)
                responsibles.append(user_profile)
            except AttributeError:
                pass
            except ObjectDoesNotExist:
                pass
        return responsibles

    def import_trainings(self, editor, trainings=None):
        trainings = trainings if trainings else self.get_trainings_from_csv_file()
        for training in trainings:
            try:
                Training.objects.get(date=training['date'])
                continue
            except ObjectDoesNotExist:
                pass

            t = Training.objects.create(
                date=training['date'],
                subject=training['subject'],
                note=training['note'],
            )
            t.responsibles = training['responsibles']
            t.creation_date = timezone.now()
            t.last_update = timezone.now()
            t.editor_id = editor.id
            t.save()
