from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Submit
from base.models import Mission, BreathingProtectionTraining, Message, UserProfile, Training


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ('number', 'alarm_time', 'keyword', 'description', 'volume', 'concerned', 'name',
                  'street', 'location', 'signal', 'vehicles', 'firefighters')

        widgets = {
            'vehicles': FilteredSelectMultiple(_('Vehicles'), is_stacked=False),
            'firefighters': FilteredSelectMultiple(_('Firefighters'), is_stacked=False),
        }

    def __init__(self, *args, **kwargs):
        super(MissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'number', 'alarm_time', 'keyword', 'description', 'volume', 'concerned', 'name',
            'street', 'location', 'signal', 'vehicles', 'firefighters',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )


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
            'date', 'location', 'participants',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )
        self.fields['participants'].queryset = UserProfile.objects.filter(
            breathing_protection_carrier=True)


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('date', 'subject', 'note', 'responsibles')

        widgets = {
            'responsibles': FilteredSelectMultiple(_('Responsibles'), is_stacked=False),
        }

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'date', 'subject', 'note', 'responsibles',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )


class BPCarrierForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'next_medical_examination_date',
                  'next_breathing_protection_training_date')

    def __init__(self, *args, **kwargs):
        super(BPCarrierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user', 'next_medical_examination_date', 'next_breathing_protection_training_date',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].widget = forms.HiddenInput()
        else:
            self.fields['user'].queryset = User.objects.filter(
                user__breathing_protection_carrier=False)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'text', 'expiration_date')

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'subject', 'text','expiration_date',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )
