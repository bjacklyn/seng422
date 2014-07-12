from django import forms
from django.contrib.auth.models import User, Group
from surveys.models import Survey
from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class CreateSurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		exclude = ('creator', 'date_created')
		widgets = {
            'description': forms.Textarea(attrs={'rows':4})
        }        

	def __init__(self, *args, **kwargs):
		disabled = kwargs.pop('disabled', False)
		super(CreateSurveyForm, self).__init__(*args, **kwargs)

        # Add form-control class to all fields
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
			
			if disabled:
				self.fields[field].widget.attrs['disabled'] = 'disabled'

        # Remove default empty label "------" and only show user's in surveyor group
		self.fields['assignee'].empty_label = None
		self.fields['assignee'].queryset = User.objects.filter(groups__name="Surveyor")
		
		# Plan Title ----------------------------------------------------------------------------
		self.fields['plan_title_type_of_plan'].label = "Type of Plan"
		self.fields['plan_title_legal_description'].label = "Legal Description & registered plan no."
		self.fields['plan_title_bcgs_no'].label = "BCGS NO."
		self.fields['plan_title_scale_and_bar'].label = "Appropriate Scale & Bar, including intended plot size"
		self.fields['plan_title_legend'].label = "Legend explaining all symbols and non-standard abbreviations"
		self.fields['plan_title_bearing'].label = "Bearing derivation and reference"
		self.fields['plan_title_notation'].label = "Notation: bearings to BTs are magnetic or planned bearings"
		self.fields['plan_title_north_point'].label = "North Point"

		self.fields['plan_title_type_of_plan'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_legal_description'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_bcgs_no'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_scale_and_bar'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_legend'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_bearing'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_notation'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['plan_title_north_point'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		
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
		self.fields['main_body_of_plan_unsurveyed_land'].label = "Label Un-surveyed Crown Land including theoretical or unsurveyed portions of townships "
		
		self.fields['main_body_of_plan_apporopriate_designation'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_essential_dimensions'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_gsi_rule3'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_boundaries_reestablished'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_sufficient_ties'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_monumentation'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_dedicated_road'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_hooked_parcels'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_new_dedicated_road'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_no_text_2mm'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_plotting_scale'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_bold_outline'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_existing_rw'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_bearing_trees_details'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_radius'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_railway_plan'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_water_body_access'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))
		self.fields['main_body_of_plan_unsurveyed_land'].widget = forms.RadioSelect(choices=Survey.SURVEY_CHOICES, renderer=HorizontalRadioRenderer, attrs=self.get_disabled(disabled))

	def get_disabled(self, disabled=False):
		if disabled:
			return {'disabled': 'disabled'}
		else:
			return {}