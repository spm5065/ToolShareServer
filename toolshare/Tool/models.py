from django.db import models
from django.contrib.auth.models import User
from Shed.models import Shed
from share_user.models import ShareUser



class Tool(models.Model):
    borrower = models.ForeignKey(User, related_name='tool_borrower', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='tool_owner', blank=True, null=True)
    identifier = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    toolname = models.CharField(max_length=100)
    ownershed = models.ForeignKey(Shed, blank=True, null=True, related_name='tools')
    shared = models.BooleanField(default=False)
    borrows = models.IntegerField(default=0, blank=True, null=True)
    requests = models.IntegerField(default=0, blank=True, null=True)
    #tool_image = models.ImageField("Tool Pic", upload_to="/static/img/tools/", blank=True, null=True)
    tool_states = (('A', 'Available'), ('U', 'Unavailable'), ('B', 'Borrowed'), ('R', 'Returned'),
                   ('P', 'Pickup'), ('D', 'Damaged'), ('Q', 'Requested'),
    )
    status = models.CharField(max_length=1, choices=(tool_states or None), default='U', blank=True, null=True)

    class Meta:
        unique_together = ('toolname', 'identifier',)

    def __str__(self):
        return self.toolname

    def get_status_name(self):
        if self.status == 'A':
            return 'Available'
        elif self.status == 'U':
            return 'Unavailable'
        elif self.status == 'B':
            return 'Borrowed'
        elif self.status == 'R':
            return 'Returned'
        elif self.status == 'P':
            return 'Pickup'
        elif self.status == 'D':
            return 'Damaged'
        elif self.status == 'Q':
            return 'Requested'
        else:
            return

    # Error Message for unique_together of toolname and identifier
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('toolname', 'identifier'):
            return 'There is already a Tool with the same Name and Identifier'
        else:
            return super(Tool, self).unique_error_message(model_class, unique_check)