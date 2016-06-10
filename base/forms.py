from django import forms
from base.models import Mission


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'
