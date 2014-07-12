from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    # Mandatory fields ----------------------------------------------------------------------------
    creator = models.ForeignKey(User, editable=False, blank=False, related_name='survey_creator')
    assignee = models.ForeignKey(User, blank=False, related_name='survey_assignee')

    date_created = models.DateTimeField('date created', editable=False, auto_now_add=True)

    title = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=False)
    land_district = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=False)

    file_number = models.PositiveIntegerField(blank=False)

    # Plan Title ----------------------------------------------------------------------------
    SURVEY_CHOICES = (
        ('U', 'Unanswered'),
        ('Y', 'Yes'),
        ('N', 'N/A'),
    )

    #plan_title_type_of_plan = models.CharField(max_length=1, choices=SURVEY_CHOICES, blank=False, default='U')
    #plan_title_legal_description = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_bcgs_no = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_scale_and_bar = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_legend = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_bearing = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_notation = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    #plan_title_north_point = models.CharField(max_length=1, choices=SURVEY_CHOICES)
    
