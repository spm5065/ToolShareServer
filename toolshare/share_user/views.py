from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from share_user.models import ShareUser
from postman.api import pm_write
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.contrib.auth.views import password_change
from share_user.forms import ShareUserRegisterForm, changePassForm, ChangeNamesForm, ChangeEmailForm, ChangeAddressForm, TestForm

# User Login View
def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            #This authenticates the user
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    #This logs him in
                    login(request, user)
                else:
                    return render(request, 'index.html', {'error_message': "This user is no longer active.  Please message an admin to activate your account."})
            else:
                return render(request, 'index.html', {'error_message': "Wrong username or password"})
    return HttpResponseRedirect("/")

# User Logout View
def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')

# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = ShareUserRegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                share_user = ShareUser.objects.get_or_create(user=new_user)
                share_user[0].zipcode = form.cleaned_data['zipcode']
                share_user[0].street_address = form.cleaned_data['street_address']
                share_user[0].city = form.cleaned_data['city']
                share_user[0].state = form.cleaned_data['state']
                share_user[0].save()
                new_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, new_user)
                return HttpResponseRedirect('/')
        else:
            form = ShareUserRegisterForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('registration/registration_form.html', context)
    else:
        return HttpResponseRedirect('/')

def edit_profile(request):
    return render(request, 'share_user/profile_edit.html')

def change_user_names(request):
    if request.method == "POST":
        form = ChangeNamesForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            url = reverse('accounts:profile')
            return HttpResponseRedirect(url)
    else:
        form = ChangeNamesForm(instance=request.user)
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('share_user/change_user_names.html', context)

def change_user_email(request):
    if request.method == "POST":
        form = ChangeEmailForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            url = reverse('accounts:profile')
            return HttpResponseRedirect(url)
    else:
        form = ChangeEmailForm(instance=request.user)
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('share_user/change_user_email.html', context)

class UpdateShareUser(UpdateView):
    model = ShareUser
    fields = ['zipcode', 'street_address', 'city', 'state']
    success_url = '/accounts/profile/'
    template_name = 'share_user/change_user_address.html'

def test_msg_send(request):
    if request.method == 'POST':
        form = TestForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            pm_write(
                sender=request.user,
                recipient=User.objects.get(username=recipient),
                subject=subject,
                body=body)
            return HttpResponseRedirect(reverse('postman_inbox'))  # Redirect after POST
    else:
        form = TestForm()  # An unbound form

    return render(request, 'share_user/test.html', {'form': form})