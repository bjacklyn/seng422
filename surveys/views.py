from surveys.models import Survey
from surveys.forms import SurveyRequirementsForm, SurveyInfoForm, SurveyAnswersForm
from surveys.decorators import group_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse

@group_required('Manager', 'Surveyor')
@login_required(login_url='/')
def list_surveys(request):
	template = loader.get_template('surveys/surveys_list_page.html')

	surveys = None
	if request.user.groups.all()[0].name == 'Manager':
		surveys = Survey.objects.filter(info__creator_id=request.user.id)
	else:
		surveys = Survey.objects.filter(info__assignee_id=request.user.id)

	context = RequestContext(request, {
            'user': request.user,
			'group': request.user.groups.all()[0].name,
			'surveys': surveys
            })

	return HttpResponse(template.render(context))

@csrf_protect
@group_required('Manager')
@login_required(login_url='/')
def create_survey(request):
	template = loader.get_template('surveys/create_survey_page.html')

	survey_info_form = SurveyInfoForm
	survey_requirements_form = SurveyRequirementsForm

	if request.method == 'POST':
		survey_info_form = SurveyInfoForm(request.POST)
		survey_requirements_form = SurveyRequirementsForm(request.POST)

		if survey_info_form.is_valid() and survey_requirements_form.is_valid():
			survey = Survey()
			
			survey.info = survey_info_form.save()
			survey.requirements = survey_requirements_form.save()
			
			survey.save()
			return HttpResponseRedirect(reverse('list_surveys'))

	context = RequestContext(request, {
			'group': request.user.groups.all()[0].name,
			'user_id': request.user.id,
			'survey_info_form': survey_info_form,
			'survey_requirements_form': survey_requirements_form,
			'page_label': 'Create a new survey',
			'cancel_button_text': 'Cancel',
			'show_create_button': True,
			'create_button_text': 'Create'
            })

	return HttpResponse(template.render(context))

@csrf_protect
@group_required('Manager', 'Surveyor')
@login_required(login_url='/')
def display_survey(request, survey_id):
	group = request.user.groups.all()[0].name

	# Get the survey from the database
	survey = None
	try:
		if group == 'Manager':
			survey = Survey.objects.get(id=survey_id, info__creator_id=request.user.id)
		else:
			survey = Survey.objects.get(id=survey_id, info__assignee_id=request.user.id)
	except Survey.DoesNotExist:
		 raise Http404

	# User does not have access to this survey
	if survey is None:
		return HttpResponseForbidden('You do not have access to this survey')

	disabled = False if group == 'Surveyor' and survey.status != Survey.SURVEY_COMPLETE else True

	survey_info_form = SurveyInfoForm(instance=survey.info, disabled=True)
	survey_requirements_form = SurveyRequirementsForm(instance=survey.requirements)
	survey_answers_form = SurveyAnswersForm(instance=survey.answers, disabled=disabled)

	if request.method == 'POST':
		survey_answers_form = SurveyAnswersForm(request.POST, instance=survey.answers, survey_requirements=survey.requirements)
		if survey_answers_form.is_valid():
			survey.status = Survey.SURVEY_COMPLETE
			survey.answers = survey_answers_form.save()
			survey.save()
		
			# re-render survey answers with radio buttons disabled
			survey_answers_form = SurveyAnswersForm(instance=survey.answers, survey_requirements=survey.requirements, disabled=True)

	template = loader.get_template('surveys/view_survey_page.html')

	context = RequestContext(request, {
		'group': group,
		'survey_answers_form': survey_answers_form,
		'survey_requirements_form': survey_requirements_form,
		'survey_info_form': survey_info_form,		
		'page_label': 'Survey ',
		'survey_id': survey_id,
		'survey_completed': True if survey.status == 'C' else False,
		'cancel_button_text': 'Back',
		'show_edit_button': True if group == 'Manager' else False,
		'edit_button_text': 'Edit Survey',
		'show_map_and_weather_button': True
	})

	return HttpResponse(template.render(context))

@csrf_protect
@group_required('Manager')
@login_required(login_url='/')
def edit_survey(request, survey_id):
	# Get the survey from the database
	survey = None
	try:
		survey = Survey.objects.get(id=survey_id, info__creator_id=request.user.id)
	except Survey.DoesNotExist:
		 raise Http404

	# User does not have access to this survey
	if survey is None:
		return HttpResponseForbidden('You do not have access to this survey')

	template = loader.get_template('surveys/create_survey_page.html')

	survey_requirements_form = SurveyRequirementsForm(instance=survey.requirements)
	survey_info_form = SurveyInfoForm(instance=survey.info)

	if request.method == 'POST':
		survey_requirements_form = SurveyRequirementsForm(request.POST, instance=survey.requirements)
		survey_info_form = SurveyInfoForm(request.POST, instance=survey.info)

		if survey_requirements_form.is_valid() and survey_info_form.is_valid():
			
			survey.info = survey_info_form.save()
			survey.requirements = survey_requirements_form.save()
			survey.save()
			return HttpResponseRedirect(reverse('display_survey', args=(survey_id,)))

	context = RequestContext(request, {
			'group': request.user.groups.all()[0].name,
			'user_id': request.user.id,
            'survey_requirements_form': survey_requirements_form,
			'survey_info_form': survey_info_form,	
			'page_label': 'Edit survey',
			'cancel_button_text': 'Cancel',
			'show_create_button': True,
			'create_button_text': 'Update'
            })

	return HttpResponse(template.render(context))

@csrf_protect
@group_required('Manager')
@login_required(login_url='/')
def delete_surveys(request):
	if request.method == 'POST':
		survey_ids = request.POST.getlist('checked_surveys')

		for id in survey_ids:
			Survey.objects.filter(id=id, info__creator_id=request.user.id).delete()

	return HttpResponseRedirect(reverse('list_surveys'))

@group_required('Manager', 'Surveyor')
@login_required(login_url='/')
def cancel_create_survey(request):
	return HttpResponseRedirect(reverse('list_surveys'))

@csrf_protect
@group_required('Manager')
@login_required(login_url='/')
def reopen_survey(request):
	if request.method == 'POST':
		survey_id = request.POST.get('survey')
		survey = Survey.objects.get(pk=survey_id, info__creator_id=request.user.id)

		if survey is not None:
			survey.status = Survey.SURVEY_INCOMPLETE
			survey.save()

	return HttpResponseRedirect(reverse('display_survey', args=(survey_id,)))
