from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@login_required
def index(request):
	
	template = loader.get_template('surveys/surveys_list_page.html')
	
	context = RequestContext(request, {
            'user': request.user,
			'group': request.user.groups.all()[0].name,
			
			#using the user list for now
			'surveys': User.objects.all()
			
            })
	
	if request.user.groups.all()[0].name == "Manager":
		pass
		#return HttpResponse('Welcome Manager %s!' % request.user.username)
	else:
		pass
		#return HttpResponse('Welcome Surveyor %s!' % request.user.username)

	return HttpResponse(template.render(context))

def create(request):
	return HttpResponse('Create your survey HERE!!! %s!' % request.user.username)

@csrf_protect
def delete(request):
	checkboxes = request.POST.getlist('checked_surveys')
	return HttpResponse('Delete your survey HERE!!! %s!' % checkboxes)
	
def display(request):
	return HttpResponse('Your survey is displayed HERE!!! %s!' % request.user.username)