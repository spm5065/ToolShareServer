from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from share_user.models import ShareUser
from django.core.validators import RegexValidator


class ShareUserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    zipcode_regex = RegexValidator(r'^\d{5}(?:[-\s]\d{4})?$', 'Only zipcode valid characters are allowed.')
    zipcode = forms.CharField(required=True, max_length=5, validators=[zipcode_regex],
                              error_messages={'required': 'Zipcode is required'})
    street_address = forms.CharField(required=True, max_length=200,
                                     error_messages={'max_length': 'Street Address must be less than 200 characters',
                                                     'required': 'Street Address is required'})
    city = forms.CharField(max_length=100, required=True,
                           error_messages={'max_length': 'City must be less than 100 characters',
                                           'required': 'City is required'})
    all_50_states = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                     ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District Of Columbia'),
                     ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
                     ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
                     ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
                     ('MN', 'Minnesota'),
                     ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
                     ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
                     ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
                     ('OR', 'Oregon'),
                     ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                     ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
                     ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    )
    state = forms.ChoiceField(choices=all_50_states, required=True,
                            error_messages={'required': 'You must select a State'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('That email address is already in use.')
        return email


class changePassForm(PasswordChangeForm):
    class Meta:
        model = User


class ChangeNamesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ChangeAddressForm(forms.ModelForm):
    class Meta:
        model = ShareUser
        fields = ['street_address', 'city', 'state', 'zipcode']


class TestForm(forms.Form):
    recipient = forms.CharField()  # recipient's username for query lookup
    subject = forms.CharField(max_length=100)
    body = forms.CharField()
