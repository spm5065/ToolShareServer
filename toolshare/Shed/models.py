from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import Tool

class Shed(models.Model):
    Street_Address = models.CharField(max_length=200)
    zipcode_regex = RegexValidator(r'^\d{5}(?:[-\s]\d{4})?$', 'Only zipcode valid characters are allowed.')
    Zip_Code = models.CharField(max_length=5, validators=[zipcode_regex])  # Must be charfield to save leading 0's
    City = models.CharField(max_length=100)
    States_all_50 = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
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
    State = models.CharField(max_length=2, choices=States_all_50)
    shed_Name = models.CharField(max_length=40, unique=True, error_messages={'unique': 'A Shed with this name already exists.'})
    Shed_Owner = models.ForeignKey(User, related_name='shed_owner', blank=True, null=True)
    description = models.CharField(max_length=500)
    uses = models.IntegerField(default=0, blank=True, null=True)
    coordinators = models.ManyToManyField(User, related_name='staff_sheds', blank=True, null=True, default=None)
    # shed_image = models.ImageField(upload_to="/images", blank=True, null=True)

    def __str__(self):
        return self.shed_Name

    def get_tool_list(self):
        return Tool.models.Tool.objects.filter(ownershed=self.pk)

class createShedForm(ModelForm):
    class Meta:
        model = Shed
        # fields = ['Street_Address','Zip_Code','City','State','shed_Name','description']
        exclude = ['States_all_50']
