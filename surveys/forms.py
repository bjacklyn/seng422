from django import forms
from django.forms.widgets import Select
from django.contrib.auth.models import User, Group
from surveys.models import Survey, SurveyAnswers, SurveyRequirements, SurveyInfo
from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class SurveyForm(forms.ModelForm):
	def get_disabled(self, disabled=False):
		if disabled:
			return {'disabled': 'disabled'}
		else:
			return {}

	def __init__(self, *args, **kwargs):
		disabled = kwargs.pop('disabled', False)
		super(SurveyForm, self).__init__(*args, **kwargs)
		
        # Add form-control class to all fields
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
			
			if disabled:
				self.fields[field].widget.attrs['disabled'] = 'disabled'
				
			# Change all checklist dropdown fields to radioselects
			if self.fields[field].widget.__class__.__name__ == Select().__class__.__name__ and not field.startswith("assignee"):
				if field.endswith("completed"):
					self.fields[field].widget = forms.RadioSelect(choices=SurveyAnswers.SURVEY_COMPLETE_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
				else:
					self.fields[field].widget = forms.RadioSelect(choices=SurveyRequirements.SURVEY_CREATE_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		

class SurveyInfoForm(SurveyForm):
	class Meta: 
		model = SurveyInfo
		exclude = ('date_created', 'status',)
		widgets = {
            'description': forms.Textarea(attrs={'rows':4})
        }
		
	def __init__(self, *args, **kwargs):
		super(SurveyInfoForm, self).__init__(*args, **kwargs)

        # Remove default empty label "------" and only show user's in surveyor group
		self.fields['assignee'].empty_label = None
		self.fields['assignee'].queryset = User.objects.filter(groups__name="Surveyor")
		
class SurveyAnswersForm(SurveyForm):
	class Meta:
		model = SurveyAnswers
		fields = '__all__'
		
	def __init__(self, *args, **kwargs):
		super(SurveyAnswersForm, self).__init__(*args, **kwargs)
		
		# Plan Title ----------------------------------------------------------------------------
		self.fields['plan_title_type_of_plan_completed'].label = "Type of Plan"
		self.fields['plan_title_legal_description_completed'].label = "Legal Description & registered plan no."
		self.fields['plan_title_bcgs_no_completed'].label = "BCGS NO."
		self.fields['plan_title_scale_and_bar_completed'].label = "Appropriate Scale & Bar, including intended plot size"
		self.fields['plan_title_legend_completed'].label = "Legend explaining all symbols and non-standard abbreviations"
		self.fields['plan_title_bearing_completed'].label = "Bearing derivation and reference"
		self.fields['plan_title_notation_completed'].label = "Notation: bearings to BTs are magnetic or planned bearings"
		self.fields['plan_title_north_point_completed'].label = "North Point"
		
		# Main Body of Plan ----------------------------------------------------------------------------
		self.fields['main_body_of_plan_apporopriate_designation_completed'].label = "Appropriate designation for title or Interest parcels (e.g. Lot Number)"
		self.fields['main_body_of_plan_essential_dimensions_completed'].label = "All essential dimensions given and closure calculated"
		self.fields['main_body_of_plan_gsi_rule3_completed'].label = "Title & Interest Parcel Area or Volume correct & to required precision-GSI Rule 3"
		self.fields['main_body_of_plan_boundaries_reestablished_completed'].label = "Boundaries reestablished and/or lots divided in accordance with Land Survey Act"
		self.fields['main_body_of_plan_sufficient_ties_completed'].label = "Sufficient ties to evidence of previous surveys"
		self.fields['main_body_of_plan_monumentation_completed'].label = "Monumentation labelled and correct - GSI Rule 1-2 to 1-7"
		self.fields['main_body_of_plan_dedicated_road_completed'].label = "Read or 'Lane' and name, when available, where road is being dedicated"
		self.fields['main_body_of_plan_hooked_parcels_completed'].label = "Remember to check for hooked parcels, part parcels and remainders"
		self.fields['main_body_of_plan_new_dedicated_road_completed'].label = "New Dedicated Road or RW fully dimensioned with widths indicated-GSI Rule "
		self.fields['main_body_of_plan_no_text_2mm_completed'].label = "No text less than 2mm"
		self.fields['main_body_of_plan_plotting_scale_completed'].label = "Plotting to scale and drafting legible - GSI Rule 3-2 & 3-3"
		self.fields['main_body_of_plan_bold_outline_completed'].label = "Bold outline 1.0 - 1.5 mm centered on boundary (including any detail drawings)"
		self.fields['main_body_of_plan_existing_rw_completed'].label = "Existing R/W, Easement or Covenant boundaries shown with broken lines - GSI Rule 3-4"
		self.fields['main_body_of_plan_bearing_trees_details_completed'].label = "Details of bearing trees and ancillary evidence found and made - GSI Rule 3-4"
		self.fields['main_body_of_plan_radius_completed'].label = "Radius, arc, radial bearings for each curve point - GSI Rule 3-4"
		self.fields['main_body_of_plan_railway_plan_completed'].label = "Railway plan in un-surveyed land has district lot number assigned"
		self.fields['main_body_of_plan_water_body_access_completed'].label = "Access to water body where applicable - LTA s75(1)"
		self.fields['main_body_of_plan_unsurveyed_land_completed'].label = "Label Un-surveyed Crown Land including theoretical or unsurveyed portions of townships"

		# Scenery ----------------------------------------------------------------------------
		self.fields['scenery_status_adjacent_roads_completed'].label = "Check status of adjacent roads. Have they all been dedicated?"
		self.fields['scenery_parcel_boundaries_completed'].label = "Parcel boundaries (incl. highway, roads and railway) shown with solid lines - Rule 3-4(2)(g)"
		self.fields['scenery_description_surrounding_lands_completed'].label = "Description(s) given for all surrounding lands - GSI Rule 3-4(1)(r)"
		self.fields['scenery_primary_parcel_designations_completed'].label = "Primary parcel designations prominent in body of plan (use 'DL' not 'Lot') - Rule 10-14"
		self.fields['scenery_existing_road_names_completed'].label = "Existing Road Names shown - GSI Rule 3-4"
		self.fields['scenery_roads_trails_seismic_lines_completed'].label = "Roads, Trails, and Seismic Lines shown and labelled with width and posted as required"
		self.fields['scenery_rem_added_completed'].label = "'Rem' added on lot and 'portion of' or 'part of' in title where appropriate"

		# Deposit Statement ----------------------------------------------------------------------------
		self.fields['deposit_statement_plan_lies_within_completed'].label = "Plan lies within (Regional District) statement - GSI Rule 3-4"
		self.fields['deposit_statement_leave_seven_cm_completed'].label = "Leave 7 cm 12 cm clear space in top right corner for Registrar's notation pursuant to S 56 LTA"

		# Integrated Survey Area ----------------------------------------------------------------------------
		self.fields['integrated_survey_area_grid_bearing_completed'].label = "Grid bearing notation; ISA name and number, datum and bearing derivation - GSI Rule 5-7"
		self.fields['integrated_survey_area_control_monuments_tied_completed'].label = "Control monuments tied in accordance with GSI Rules 5-4(2)"
		self.fields['integrated_survey_area_meets_accuracy_completed'].label = "Meets accuracy standards of integrated legal survey - GSI Rule 5-4 (3) & (4)"
		self.fields['integrated_survey_area_control_monuments_shown_completed'].label = "Control monuments shown on plan with required symbol and respective designation - GSI Rule 5-7(2)"

		# Miscellaneous ----------------------------------------------------------------------------
		self.fields['miscellaneous_spelling_check_completed'].label = "Spelling check"
		self.fields['miscellaneous_standard_plan_size_completed'].label = "Standard plan size - GSI Rule 3-1"
		self.fields['miscellaneous_oriented_north_completed'].label = "If practical, top of plan orientated north - GSI Rule 3-3(5)"
		self.fields['miscellaneous_notation_completed'].label = "Notation regarding existing records that plan is compiled from"

		# Electronic Plan ----------------------------------------------------------------------------
		self.fields['electronic_plan_plan_image_completed'].label = "Plan Image created with Adobe 6.0 or higher with minimum 600 dpi resolution - GSI Rule 3-1 (1)"
		self.fields['electronic_plan_plan_features_completed'].label = "All plan features black ink on white background with no ornate fonts - GSI Rule 3-3(1)"
		self.fields['electronic_plan_no_signatures_completed'].label = "No signatures on plan - GSI Rule 3-3(7)"
		self.fields['electronic_plan_plan_complies_completed'].label = "Plan complies with all standards for electronic submissions approved by S.G. GSI Rule 3-3 (12)"
		
		
class SurveyRequirementsForm(SurveyForm):
	class Meta:
		model = SurveyRequirements
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(SurveyRequirementsForm, self).__init__(*args, **kwargs)
		
		# Plan Title ----------------------------------------------------------------------------
		self.fields['plan_title_type_of_plan'].label = "Type of Plan"
		self.fields['plan_title_legal_description'].label = "Legal Description & registered plan no."
		self.fields['plan_title_bcgs_no'].label = "BCGS NO."
		self.fields['plan_title_scale_and_bar'].label = "Appropriate Scale & Bar, including intended plot size"
		self.fields['plan_title_legend'].label = "Legend explaining all symbols and non-standard abbreviations"
		self.fields['plan_title_bearing'].label = "Bearing derivation and reference"
		self.fields['plan_title_notation'].label = "Notation: bearings to BTs are magnetic or planned bearings"
		self.fields['plan_title_north_point'].label = "North Point"
		
		# Main Body of Plan ----------------------------------------------------------------------------
		self.fields['main_body_of_plan_apporopriate_designation'].label = "Appropriate designation for title or Interest parcels (e.g. Lot Number)"
		self.fields['main_body_of_plan_essential_dimensions'].label = "All essential dimensions given and closure calculated"
		self.fields['main_body_of_plan_gsi_rule3'].label = "Title & Interest Parcel Area or Volume correct & to required precision-GSI Rule 3"
		self.fields['main_body_of_plan_boundaries_reestablished'].label = "Boundaries reestablished and/or lots divided in accordance with Land Survey Act"
		self.fields['main_body_of_plan_sufficient_ties'].label = "Sufficient ties to evidence of previous surveys"
		self.fields['main_body_of_plan_monumentation'].label = "Monumentation labelled and correct - GSI Rule 1-2 to 1-7"
		self.fields['main_body_of_plan_dedicated_road'].label = "Read or 'Lane' and name, when available, where road is being dedicated"
		self.fields['main_body_of_plan_hooked_parcels'].label = "Remember to check for hooked parcels, part parcels and remainders"
		self.fields['main_body_of_plan_new_dedicated_road'].label = "New Dedicated Road or RW fully dimensioned with widths indicated-GSI Rule "
		self.fields['main_body_of_plan_no_text_2mm'].label = "No text less than 2mm"
		self.fields['main_body_of_plan_plotting_scale'].label = "Plotting to scale and drafting legible - GSI Rule 3-2 & 3-3"
		self.fields['main_body_of_plan_bold_outline'].label = "Bold outline 1.0 - 1.5 mm centered on boundary (including any detail drawings)"
		self.fields['main_body_of_plan_existing_rw'].label = "Existing R/W, Easement or Covenant boundaries shown with broken lines - GSI Rule 3-4"
		self.fields['main_body_of_plan_bearing_trees_details'].label = "Details of bearing trees and ancillary evidence found and made - GSI Rule 3-4"
		self.fields['main_body_of_plan_radius'].label = "Radius, arc, radial bearings for each curve point - GSI Rule 3-4"
		self.fields['main_body_of_plan_railway_plan'].label = "Railway plan in un-surveyed land has district lot number assigned"
		self.fields['main_body_of_plan_water_body_access'].label = "Access to water body where applicable - LTA s75(1)"
		self.fields['main_body_of_plan_unsurveyed_land'].label = "Label Un-surveyed Crown Land including theoretical or unsurveyed portions of townships"

		# Scenery ----------------------------------------------------------------------------
		self.fields['scenery_status_adjacent_roads'].label = "Check status of adjacent roads. Have they all been dedicated?"
		self.fields['scenery_parcel_boundaries'].label = "Parcel boundaries (incl. highway, roads and railway) shown with solid lines - Rule 3-4(2)(g)"
		self.fields['scenery_description_surrounding_lands'].label = "Description(s) given for all surrounding lands - GSI Rule 3-4(1)(r)"
		self.fields['scenery_primary_parcel_designations'].label = "Primary parcel designations prominent in body of plan (use 'DL' not 'Lot') - Rule 10-14"
		self.fields['scenery_existing_road_names'].label = "Existing Road Names shown - GSI Rule 3-4"
		self.fields['scenery_roads_trails_seismic_lines'].label = "Roads, Trails, and Seismic Lines shown and labelled with width and posted as required"
		self.fields['scenery_rem_added'].label = "'Rem' added on lot and 'portion of' or 'part of' in title where appropriate"

		# Deposit Statement ----------------------------------------------------------------------------
		self.fields['deposit_statement_plan_lies_within'].label = "Plan lies within (Regional District) statement - GSI Rule 3-4"
		self.fields['deposit_statement_leave_seven_cm'].label = "Leave 7 cm 12 cm clear space in top right corner for Registrar's notation pursuant to S 56 LTA"

		# Integrated Survey Area ----------------------------------------------------------------------------
		self.fields['integrated_survey_area_grid_bearing'].label = "Grid bearing notation; ISA name and number, datum and bearing derivation - GSI Rule 5-7"
		self.fields['integrated_survey_area_control_monuments_tied'].label = "Control monuments tied in accordance with GSI Rules 5-4(2)"
		self.fields['integrated_survey_area_meets_accuracy'].label = "Meets accuracy standards of integrated legal survey - GSI Rule 5-4 (3) & (4)"
		self.fields['integrated_survey_area_control_monuments_shown'].label = "Control monuments shown on plan with required symbol and respective designation - GSI Rule 5-7(2)"

		# Miscellaneous ----------------------------------------------------------------------------
		self.fields['miscellaneous_spelling_check'].label = "Spelling check"
		self.fields['miscellaneous_standard_plan_size'].label = "Standard plan size - GSI Rule 3-1"
		self.fields['miscellaneous_oriented_north'].label = "If practical, top of plan orientated north - GSI Rule 3-3(5)"
		self.fields['miscellaneous_notation'].label = "Notation regarding existing records that plan is compiled from"

		# Electronic Plan ----------------------------------------------------------------------------
		self.fields['electronic_plan_plan_image'].label = "Plan Image created with Adobe 6.0 or higher with minimum 600 dpi resolution - GSI Rule 3-1 (1)"
		self.fields['electronic_plan_plan_features'].label = "All plan features black ink on white background with no ornate fonts - GSI Rule 3-3(1)"
		self.fields['electronic_plan_no_signatures'].label = "No signatures on plan - GSI Rule 3-3(7)"
		self.fields['electronic_plan_plan_complies'].label = "Plan complies with all standards for electronic submissions approved by S.G. GSI Rule 3-3 (12)"
