__author__ = 'Sergio'

from django import forms
from django.forms import ModelForm
from Shed.models import Shed


class createShedForm(ModelForm):
    class Meta:
        model = Shed
        #fields = ['Street_Address','Zip_Code','City','State','shed_Name','description']
        exclude = ['States_all_50']

