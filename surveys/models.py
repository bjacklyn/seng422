from django.db import models

# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField('date created')
