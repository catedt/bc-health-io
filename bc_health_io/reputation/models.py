import django
from django.db import models


class Reputation(models.Model):
    doctorId = models.CharField(max_length=42)
    email = models.CharField(max_length=255)
    repute = models.IntegerField()

    createDate = models.DateTimeField('Reputation Created', default=django.utils.timezone.now)
    updateDate = models.DateTimeField('Reputation Updated', default=django.utils.timezone.now)

    class Meta:
        ordering = ['updateDate']
