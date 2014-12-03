from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from Shed.models import Shed
from postman import models as models2
#import Tool.models

from django.core.validators import RegexValidator

class ShareUser(models.Model):
    user = models.OneToOneField(User)
    zipcode_regex = RegexValidator(r'^\d{5}(?:[-\s]\d{4})?$', 'Only zipcode valid characters are allowed.')
    zipcode = models.CharField(max_length=5, validators=[zipcode_regex])
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
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
    state = models.CharField(max_length=2, choices=all_50_states)
    sheds = models.ManyToManyField(Shed, blank=True, null=True, related_name='reg_users')  # Sheds this user is registered in
    tools = models.ManyToManyField('Tool.Tool', blank=True, null=True)  # Tools this user owns

    def __str__(self):
        return self.user.get_username()

    def get_new_messages(self):
        msgs = models2.Message.objects.filter(recipient=self.user.id).all()
        for msg in msgs:
            if msg.read_at is None:
                return True
        if 0:
            return True
        else:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShareUser.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)