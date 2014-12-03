__author__ = 'Noah'

from django import forms


class RequestForm(forms.Form):
    start_date = forms.DateField(required=True, error_messages={'required': 'Start date must be valid and non-empty.'})
    end_date = forms.DateField(required=True, error_messages={'required': 'End date must be valid and non-empty.'})
    message = forms.CharField(required=False)
