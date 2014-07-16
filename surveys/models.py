from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    # Mandatory fields ----------------------------------------------------------------------------
    creator = models.ForeignKey(User, blank=False, related_name='survey_creator')
    assignee = models.ForeignKey(User, blank=False, related_name='survey_assignee')

    date_created = models.DateTimeField('date created', editable=False, auto_now_add=True)

    title = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=False)
    land_district = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255, blank=False)

    file_number = models.PositiveIntegerField(blank=False)


    # Survey Completion
    SURVEY_COMPLETED_CHOICES = (
        ('C', 'Complete'),
        ('I', 'Incomplete'),
    )

    completed = models.CharField(max_length=1, choices=SURVEY_COMPLETED_CHOICES, blank=False, default='I')


    # Plan Title ----------------------------------------------------------------------------
    SURVEY_CHOICES = (
        ('U', 'Unanswered'),
        ('Y', 'Yes'),
        ('N', 'N/A'),
    )

    plan_title_type_of_plan = models.CharField(max_length=1, choices=SURVEY_CHOICES, blank=False, default='U')
    plan_title_legal_description = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_bcgs_no = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_scale_and_bar = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_legend = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_bearing = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_notation = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    plan_title_north_point = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
	
	# Main Body of Plan ----------------------------------------------------------------------------
    main_body_of_plan_apporopriate_designation = models.CharField(max_length=1, choices=SURVEY_CHOICES, blank=False, default='U')
    main_body_of_plan_essential_dimensions = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_gsi_rule3 = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_boundaries_reestablished = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_sufficient_ties = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_monumentation = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_dedicated_road = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_hooked_parcels = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_new_dedicated_road = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_no_text_2mm = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_plotting_scale = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_bold_outline = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_existing_rw = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_bearing_trees_details = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_radius = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_railway_plan = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_water_body_access = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    main_body_of_plan_unsurveyed_land = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')

	# Scenery ----------------------------------------------------------------------------
    scenery_status_adjacent_roads = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_parcel_boundaries = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_description_surrounding_lands = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_primary_parcel_designations = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_existing_road_names = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_roads_trails_seismic_lines = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    scenery_rem_added = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')

	# Deposit Statement ----------------------------------------------------------------------------
    deposit_statement_plan_lies_within = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    deposit_statement_leave_seven_cm = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')

	# Integrated Survey Area ----------------------------------------------------------------------------
    integrated_survey_area_grid_bearing = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    integrated_survey_area_control_monuments_tied = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    integrated_survey_area_meets_accuracy = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    integrated_survey_area_control_monuments_shown = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')

	# Miscellaneous ----------------------------------------------------------------------------
    miscellaneous_spelling_check = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    miscellaneous_standard_plan_size = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    miscellaneous_oriented_north = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    miscellaneous_notation = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')

	# Electronic Plan ----------------------------------------------------------------------------
    electronic_plan_plan_image = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    electronic_plan_plan_features = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    electronic_plan_no_signatures = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
    electronic_plan_plan_complies = models.CharField(max_length=1, choices=SURVEY_CHOICES, default='U')
