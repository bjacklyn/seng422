from surveys.forms import CreateSurveyForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from surveys.models import Survey

# Create your views here.
@login_required
def index(request):
	
	template = loader.get_template('surveys/surveys_list_page.html')
	
	surveys = None
	if request.user.groups.all()[0].name == "Manager":
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
def create(request):
	template = loader.get_template('surveys/create_survey_page.html')
	
	create_survey_form = CreateSurveyForm

	if request.method == 'POST':
		create_survey_form = CreateSurveyForm(request.POST)
		
		if create_survey_form.is_valid():
			survey = create_survey_form.save(commit=False)
			survey.creator = request.user
			survey.save()
			return HttpResponseRedirect(reverse('index'))
	
	context = RequestContext(request, {
            'create_survey_form': create_survey_form
            })

	return HttpResponse(template.render(context))

@login_required
@csrf_protect
def delete(request):
	survey_ids = request.POST.getlist('checked_surveys')
	
	for id in survey_ids:
		Survey.objects.filter(id=id).delete()

	return HttpResponseRedirect(reverse('index'))

@login_required
def display(request):
	return HttpResponse('Your survey is displayed HERE!!! %s!' % request.user.username)
