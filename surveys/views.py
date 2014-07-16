from surveys.models import Survey
from surveys.forms import CreateSurveyForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse

@login_required
def list_surveys(request):
	template = loader.get_template('surveys/surveys_list_page.html')

	surveys = None
	if request.user.groups.all()[0].name == 'Manager':
		surveys = Survey.objects.filter(creator__id=request.user.id)
	else:
		surveys = Survey.objects.filter(assignee__id=request.user.id)

	context = RequestContext(request, {
            'user': request.user,
			'group': request.user.groups.all()[0].name,
			'surveys': surveys
            })

	return HttpResponse(template.render(context))

@login_required
@csrf_protect
def create_survey(request):
	# Only managers can see the create page
	group = request.user.groups.all()[0].name
	if not group == 'Manager':
		return HttpResponseForbidden()

	template = loader.get_template('surveys/create_survey_page.html')

	create_survey_form = CreateSurveyForm

	if request.method == 'POST':
		create_survey_form = CreateSurveyForm(request.POST)

		if create_survey_form.is_valid():
			survey = create_survey_form.save(commit=False)
			survey.creator = request.user
			survey.save()
			return HttpResponseRedirect(reverse('list_surveys'))

	context = RequestContext(request, {
			'group': group,
			'user_id': request.user.id,
			'create_survey_form': create_survey_form,
			'page_label': 'Create a new survey',
			'show_submit_button': True,
			'cancel_button_text': 'Cancel',
			'show_create_button': True,
			'submit_button_text': 'Create'
            })

	return HttpResponse(template.render(context))

@login_required
def display_survey(request, survey_id):
	group = request.user.groups.all()[0].name

	# Get the survey from the database
	survey = None
	try:
		if group == 'Manager':
			survey = Survey.objects.get(id=survey_id, creator__id=request.user.id)
		else:
			survey = Survey.objects.get(id=survey_id, assignee__id=request.user.id)
	except Survey.DoesNotExist:
		 raise Http404

	# User does not have access to this survey
	if survey is None:
		return HttpResponseForbidden()

	template = loader.get_template('surveys/create_survey_page.html')

	create_survey_form = CreateSurveyForm(
							instance=survey,
							disabled=True)
	
	context = RequestContext(request, {
		'group': group,
		'create_survey_form': create_survey_form,
		'page_label': 'Survey ',
		'survey_id': survey_id,
		'survey_completed': True if survey.completed == 'C' else False,
		'cancel_button_text': 'Back',
		'show_edit_button': True if group == 'Manager' else False,
		'edit_button_text': 'Edit Survey',
		'show_map_and_weather_button': True
	})

	return HttpResponse(template.render(context))

@login_required
@csrf_protect
def edit_survey(request, survey_id):
	# Only managers can edit surveys
	group = request.user.groups.all()[0].name
	if not group == 'Manager':
		return HttpResponseForbidden()

	# Get the survey from the database
	survey = None
	try:
		survey = Survey.objects.get(id=survey_id, creator__id=request.user.id)
	except Survey.DoesNotExist:
		 raise Http404

	# User does not have access to this survey
	if survey is None:
		return HttpResponseForbidden()

	template = loader.get_template('surveys/create_survey_page.html')

	create_survey_form = None

	if request.method == 'POST':
		create_survey_form = CreateSurveyForm(request.POST, instance=survey)

		if create_survey_form.is_valid():
			survey = create_survey_form.save(commit=False)
			survey.creator = request.user
			survey.save()
			#return HttpResponseRedirect(reverse('list_surveys'))
			return HttpResponseRedirect(reverse('display_survey', args=(survey_id,)))
	else:
		create_survey_form = CreateSurveyForm(instance=survey)

	context = RequestContext(request, {
			'group': group,
			'user_id': request.user.id,
            'create_survey_form': create_survey_form,
			'page_label': 'Create a new survey',
			'show_submit_button': True,
			'cancel_button_text': 'Cancel',
			'show_create_button': True,
			'submit_button_text': 'Update'
            })

	return HttpResponse(template.render(context))

@login_required
@csrf_protect
def delete_surveys(request):
	# Only managers can delete surveys
	if not request.user.groups.all()[0].name == 'Manager':
		return HttpResponseForbidden()

	if request.method == 'POST':
		survey_ids = request.POST.getlist('checked_surveys')

		for id in survey_ids:
			Survey.objects.filter(id=id, creator=request.user).delete()

	return HttpResponseRedirect(reverse('list_surveys'))

@login_required
@csrf_protect
def complete_survey(request):
	if not request.user.groups.all()[0].name == 'Surveyor':
		return HttpResponseForbidden()

	if request.method == 'POST':
		survey_id = request.POST.get('survey')
		survey = Survey.objects.get(pk=survey_id)
		survey.completed = 'C'
		survey.save()

	return HttpResponseRedirect(reverse('display_survey', args=(survey_id,)))

@login_required	
def cancel_create_survey(request):
	return HttpResponseRedirect(reverse('list_surveys'))
