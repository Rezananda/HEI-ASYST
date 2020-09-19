from django.db import models
from account.models import UserProfile
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserAttendance(models.Model):

    selfassstatus = models.CharField(max_length=251, null=False)

    attendance = models.CharField(max_length=255, null=False)
    reasonNotPresent = models.CharField(max_length=255, null=False)
    otherNotPresent = models.CharField(max_length=255, null=False)

    condition = models.CharField(max_length=255, null=False)
    sickChoices = models.CharField(max_length=255, null=False)
    otherSicks = models.CharField(max_length=255, null=False)
    
    work_status = models.CharField(max_length=255, null=False)
    wfo_description = models.CharField(max_length=255, null=False)

    authors = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.authors)
