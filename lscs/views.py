from lscs.forms import SignupForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login as auth_login

def main_page(request):
    template = loader.get_template('lscs/main_page.html')
    
    login_form = AuthenticationForm
    signup_form = SignupForm
    passwordreset_form = PasswordResetForm

    if request.method == "POST":
        
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():

                # Log the user in.
                auth_login(request, login_form.get_user())
                return HttpResponseRedirect('/surveys')

        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                username = signup_form.clean_username()
                password = signup_form.clean_password2()
                user = signup_form.save()
                print 'password ' + password
                print 'user.password ' + user.password
                user = authenticate(username=username, 
                                    password=password)
                auth_login(request, user)
                return HttpResponseRedirect('/surveys')

        if 'reset' in request.POST:
            passwordreset_form = PasswordResetForm(request.POST)
            if passwordreset_form.is_valid():
                passwordreset_form.save(request=request)

    context = RequestContext(request, {
            'login_form': login_form,
            'signup_form': signup_form,
            'passwordreset_form': passwordreset_form
            })

    return HttpResponse(template.render(context))

def reset_complete(request):
    context = RequestContext(request, {})
    template = loader.get_template('lscs/password_reset_complete.html')
    return HttpResponse(template.render(context))