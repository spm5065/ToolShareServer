from django.db import models
from django.contrib.auth.models import User
from Tool.models import Tool


class BorrowRequest(models.Model):
    borrower = models.ForeignKey(User, related_name='borrower', blank=True, null=True)
    tool = models.ForeignKey(Tool, related_name='tool', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)