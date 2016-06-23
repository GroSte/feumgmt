from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Submit
from base.models import Mission, BreathingProtectionTraining


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'


class BPTrainingForm(forms.ModelForm):
    class Meta:
        model = BreathingProtectionTraining
        fields = ('date', 'location', 'participants')

        widgets = {
            'participants': FilteredSelectMultiple(_('Participants'), is_stacked=False),
        }

    def __init__(self, *args, **kwargs):
        super(BPTrainingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'date', 'location',
                'participants',
            Submit('submit', _(u'Save'), css_class='btn-common btn-save'),
            Submit('cancel', _(u'Cancel'), css_class='btn-common btn-cancel'),
        )
