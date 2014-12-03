from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
#from Shed.models import createShedForm
from Shed.forms import createShedForm
from Shed.models import Shed
from share_user.models import ShareUser
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.template.defaulttags import register
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import models
from django import forms


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    return CreateShedView(request)

def createShed(request):
    if request.method == 'POST':
        form = createShedForm(request.POST)
        if form.is_valid():
            shed = form.save(commit=False)
            shed.coordinators = None
            return HttpResponseRedirect('/')
    else:
        form = createShedForm().as_view()

    return render(request, 'Shed/createShed.html', {'form': createShedForm})

class DisplayShedView(DetailView):
    model = Shed
    template_name = 'Shed/display.html'

    def get_context_data(self, **kwargs):
        context = super(DisplayShedView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class CreateShedView(CreateView):
    #template_name = 'contact.html'
    #form_class = createShedForm
    #success_url = '/accounts/profile/'
    model = Shed
    exclude = ['States_all_50', 'uses', 'coordinators']
    success_url = '/shed/1'
    def form_valid(self, form):
        Shed = form.save(commit=False)
        Shed.Shed_Owner = User.objects.get(username=self.request.user.username)
        Shed.uses = 0
        Shed.save()
        return HttpResponseRedirect(self.success_url)

def ShedList(request, page_id=1):
    if request.user.is_authenticated():
        query_shed_list = Shed.objects.filter(Zip_Code=request.user.shareuser.zipcode)  # Gets all sheds with the same
                                                                                        # zipcode of the current user
        total = query_shed_list.count()
        num_pages = []
        for i in range(total//20 + 1):  # Create a page for every multiple of 20 result we have
            num_pages.append(i+1)
        if total % 20 == 0:  # If length is exactly a multiple of 20, remove the last page to compensate
            num_pages.pop(len(num_pages)-1)
        c_user_sheds = request.user.shareuser.sheds.all()  # Grabs all the current user's sheds to create a dict
        c_user_shed_ids = []
        for shed in c_user_sheds:
            c_user_shed_ids.append(shed.id)
        registered_dict = {}  # Dictionary to determine whether or not a user is already registered to a shed
        for shed in query_shed_list:
            if shed.id in c_user_shed_ids:
                registered_dict[shed.id] = True
            else:
                registered_dict[shed.id] = False
        # Pagination index handling
        start_index = (int(page_id) - 1) * 20
        end_index = int(page_id) * 20
        previous_page_id = int(page_id) - 1
        if previous_page_id <= 0:
            previous_page_id = 1
        next_page_id = int(page_id) + 1
        if next_page_id > (total // 20 + 1):
            next_page_id = total//20 + 1
        return render(request, 'Shed/shed_list.html', {'query_shed_list': query_shed_list[start_index:end_index],
                                                       'registered_dict': registered_dict,
                                                       'num_pages': num_pages,
                                                       'previous_page_id': previous_page_id,
                                                       'next_page_id': next_page_id})
    else:
        return render(request, 'Shed/shed_list.html')

class UpdateShedView(UpdateView):
    model = Shed
    fields = ['coordinators']
    success_url = '/shed/1'
    template_name = 'Shed/Update_Shed.html'
    def form_valid(self, form):
        shed = form.save(commit = False)
        data = form.cleaned_data
        coords = data['coordinators']
        shed_owner = shed.Shed_Owner
        current_user = User.objects.get(username=self.request.user.username)
        for y in shed.coordinators.all():
            shed.coordinators.remove(y)
        for x in coords:
            shed.coordinators.add(x)
        shed.save()
        return HttpResponseRedirect(self.get_success_url())


def MyShedList(request):
    if request.user.is_authenticated():
        query_shed_list = request.user.shareuser.sheds.all()
        return render(request, 'share_user/my_shed.html', {'query_shed_list': query_shed_list})
    else:
        return render(request, 'share_user/my_shed.html')

def register_user_with_shed(request, shed_id):
    shed_to_add = Shed.objects.get(id=shed_id)
    request.user.shareuser.sheds.add(shed_to_add)
    return ShedList(request)

def deregister_user_with_shed(request, shed_id):
    shed_to_remove = Shed.objects.get(id=shed_id)
    request.user.shareuser.sheds.remove(shed_to_remove)  # Removes the first instance, make sure you can only register
                                                         # to a shed once.
    return ShedList(request)

def shed_stats(request, pk):
    shed = Shed.objects.get(id=pk)
    return render(request, 'Shed/stats.html', {'shed': shed})