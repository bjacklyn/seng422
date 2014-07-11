from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
	if request.user.groups.all()[0].name == "Manager":
		return HttpResponse('Welcome Manager %s!' % request.user.username)
	else:
		return HttpResponse('Welcome Surveyor %s!' % request.user.username)
