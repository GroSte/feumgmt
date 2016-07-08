# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os

from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from base.models import UserProfile, Training


class Importer(object):
    mapping = {}

    character_mapping = {
        0xe4: u'ae',
        ord(u'ö'): u'oe',
        ord(u'ü'): u'ue',
        ord(u'ß'): u'ss',
    }

    def get_current_mapping(self, row):
        current_mapping = {}
        reverted_mapping = dict((v, k) for k, v in self.mapping.iteritems())
        row_pos = 1
        for field in row:
            if field in reverted_mapping:
                current_mapping[reverted_mapping[field]] = row_pos
            row_pos += 1
        return current_mapping


class UserImporter(Importer):
    mapping = {
        'last_name': 'Name',
        'first_name': 'Vorname',
        'birth_date': 'Geburt',
        'admittance_date': 'Eintritt',
        'phone_number': 'Tel.',
        'mobile_phone_number': 'Handy',
        'email': 'E-Mail',
    }

    def get_users_from_csv_file(self, file_name='config/user.csv'):
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

        users = []
        for row in rows:
            user = {}
            for field, index in current_mapping.iteritems():
                user[field] = row[index - 1]
            users.append(user)
        return users

    def import_users(self, users, editor):
        for user in users:
            first_name = unicode(user['first_name'], 'utf-8')
            last_name = unicode(user['last_name'], 'utf-8')
            username = '{0}.{1}'.format(first_name[:1], last_name)
            username = username.lower()
            username = username.translate(self.character_mapping)
            try:
                User.objects.get(username=username)
                continue
            except ObjectDoesNotExist:
                pass

            u = User.objects.create_user(username, user['email'], 'test')
            u.first_name = first_name
            u.last_name = last_name
            u.save()

            birth_date = None
            admittance_date = None
            if user['birth_date'] != '':
                birth_date = datetime.strptime(user['birth_date'], '%d.%m.%Y')
            if user['admittance_date'] != '':
                admittance_date = datetime.strptime(user['admittance_date'], '%d.%m.%Y')
            profile = UserProfile.objects.create(
                user_id=u.id,
                birth_date=birth_date,
                admittance_date=admittance_date,
                phone_number=user['phone_number'],
                mobile_phone_number=user['mobile_phone_number'],
            )
            profile.creation_date = timezone.now()
            profile.last_update = timezone.now()
            profile.editor_id = editor.id
            profile.save()


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
