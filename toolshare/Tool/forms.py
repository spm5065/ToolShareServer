__author__ = 'Sergio'

from django import forms
from django.forms import ModelForm
from Tool.models import Tool


class createShedForm(ModelForm):
    class Meta:
        model = Tool
        #fields = ['Street_Address','Zip_Code','City','State','shed_Name','description']
        exclude = ['owner', ''' 'shared',''' 'status']

class UpdateToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['shared', 'ownershed']  # OWNERSHED CANNOT BE SET BACK TO USERSHED AFTER BELONGING TO A COMMUNITY SHED

class DeleteToolForm(ModelForm):
    class Meta:
        model = Tool

class ReturnForm(forms.Form):
    giveBack = forms.BooleanField(required=True)

class ApproveForm(forms.Form):
    allow = forms.BooleanField(required=False)
    rejection_message = forms.CharField(max_length=140, required=False)

class PickupForm(forms.Form):
    pickup = forms.BooleanField(required=True)

class FixedForm(forms.Form):
    fixed = forms.BooleanField(required=False)

class CheckReturn(forms.Form):
    returned = forms.BooleanField(required=True)
    damaged = forms.BooleanField(required=False)