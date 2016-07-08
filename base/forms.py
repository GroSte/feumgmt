from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Submit
from base.models import Message


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password', 'new_password1', 'new_password2',
            Submit('submit', _(u'Save'), css_class='btn-success'),
            Submit('cancel', _(u'Cancel'), css_class='btn-abort'),
        )


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
