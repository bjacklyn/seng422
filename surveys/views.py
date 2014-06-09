from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        template = loader.get_template('surveys/surveys.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/login/')
