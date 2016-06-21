# coding=UTF-8
from django.core.serializers import base


class LoadDataWithModelState(object):
    """
    Load fixture data with migration state models.
    """

    def __init__(self, fixture):
        self.fixture = fixture

    def load(self, models, schema_editor):
        def new_get_model(model_identifier):
            """
            Helper to look up a model from an "app_label.model_name" string.
            From
            """
            try:
                return models.get_model(model_identifier)
            except (LookupError, TypeError):
                raise base.DeserializationError(
                    "Invalid model identifier: '%s'" % model_identifier)

        from django.core.serializers import python

        original_function = getattr(python, '_get_model')
        setattr(python, '_get_model', new_get_model)

        from django.core.management import call_command

        call_command('loaddata', self.fixture)

        setattr(python, '_get_model', original_function)
