from django import forms
from django.contrib.auth.models import User, Group
from surveys.models import Survey

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('assignee', 'title', 'description', 'address', 'land_district', 'file_number' # Mandatory fields
                    )
        widgets = {
            'description': forms.Textarea(attrs={'rows':4})
        }        

    def __init__(self, *args, **kwargs):
        super(CreateSurveyForm, self).__init__(*args, **kwargs)

        # Add form-control class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Remove default empty label "------" and only show user's in surveyor group
        self.fields['assignee'].empty_label = None
        self.fields['assignee'].queryset = User.objects.filter(groups__name="Surveyor")
