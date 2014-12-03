from django.shortcuts import render
from django.template import RequestContext, loader
from Tool.models import Tool
from Shed.models import Shed
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from Tool.forms import UpdateToolForm, ReturnForm, ApproveForm, PickupForm, CheckReturn, FixedForm
from django.views.generic.detail import DetailView
from django import views
from django.utils import timezone
from postman.api import pm_write
from django.db import models


def index(request):
    if request.user.is_authenticated():
        latest_tool_list = Tool.objects.filter(owner__shareuser__zipcode=request.user.shareuser.zipcode)
        return render(request, 'Tool/index.html', {'latest_tool_list': latest_tool_list})
    else:
        return render(request, 'Tool/index.html')

def requests(request):
    if request.user.is_authenticated():
        requested_tool_list = []
        tool_list = Tool.objects.filter(status='Q')
        for ptool in tool_list:
            if ptool.owner == request.user:
                requested_tool_list.append(ptool)
            if ptool.ownershed:
                if ptool.ownershed.coordinators:
                    for coor in ptool.ownershed.coordinators.all():
                        if coor == request.user:
                            requested_tool_list.append(ptool)
            if ptool.ownershed:
                if ptool.ownershed.Shed_Owner == request.user:
                    requested_tool_list.append(ptool)

                requested_tool_list.append(ptool)
    return render(request, 'Tool/requested.html', {'requested_tool_list': requested_tool_list})

def approve_request(request, pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = ApproveForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            data = form.cleaned_data
            allow = data['allow']
            if allow:
                tool.status = 'P'
                tool.borrows += 1
                tool.save()
                return HttpResponseRedirect('/tool/requested/')
            else:
                tool.status = 'A'
                tool.save()
                body = data['rejection_message']
                message = 'Your request has been denied.\n The owners message is included below.\n' + body
                pm_write(sender=request.user,
                    recipient=User.objects.get(id=tool.borrower.id),
                    subject='Tool: ' + tool.toolname + ' ',
                    body=message)
                return HttpResponseRedirect('/tool/requested/')
    else:
        form = ApproveForm()  # An unbound form
    return render(request, 'Tool/approve_request.html', {'form': form})

def returns(request):
    if request.user.is_authenticated():
        returned_tool_list = []
        tool_list = Tool.objects.filter(status='R')
        for ptool in tool_list:
            if ptool.owner == request.user:
                returned_tool_list.append(ptool)
            if ptool.ownershed:
                if ptool.ownershed.Shed_Owner == request.user and (ptool not in returned_tool_list):
                    returned_tool_list.append(ptool)
                if ptool.ownershed.coordinators:
                    for coor in ptool.ownershed.coordinators.all():
                        if coor == request.user:
                            returned_tool_list.append(ptool)
    return render(request, 'Tool/returned.html', {'returned_tool_list': returned_tool_list})

def fix(request, pk):
    if request.user.is_authenticated():
        tool = Tool.objects.get(id=pk)
        if request.method == 'POST':
            form = FixedForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                fixed = data['fixed']
                if fixed:
                    if tool.owner == request.user:
                        tool.status = 'U'
                        tool.save()
                    if tool.ownershed:
                        if tool.ownershed.Shed_Owner == request.user:
                            tool.status = 'U'
                            tool.save()
                        if tool.ownershed.coordinators:
                            for coor in tool.ownershed.coordinators.all():
                                if coor == request.user:
                                    tool.status = 'U'
                                    tool.save()
                return HttpResponseRedirect('/tool/damaged/')
        else:
            form = FixedForm()
        return render(request, 'Tool/fix.html', {'tool': tool, 'form': form})
    else:
        HttpResponseRedirect('/accounts/login')

def tool_stats(request, pk):
    tool = Tool.objects.get(id=pk)
    return render(request, 'Tool/stats.html', {'tool': tool})



def damaged(request):
    if request.user.is_authenticated():
        damaged_tool_list = []
        tool_list = Tool.objects.filter(status='D')
        for ptool in tool_list:
            if (ptool.owner == request.user) or (ptool.ownershed.Shed_Owner == request.user) or(ptool.ownershed.coordinators == request.user):
                damaged_tool_list.append(ptool)
        return render(request, 'Tool/damaged.html', {'damaged_tool_list' : damaged_tool_list})


def borrowed(request):
    if request.user.is_authenticated():
        borrowed_tool_list = []
        tool_list = Tool.objects.filter(status='B')
        for ptool in tool_list:
            if ptool.borrower == request.user:
                borrowed_tool_list.append(ptool)
    return render(request, 'Tool/borrowed.html', {'borrowed_tool_list' : borrowed_tool_list})

def return_tool(request, pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = ReturnForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            data = form.cleaned_data
            giveBack = data['giveBack']
            if giveBack:
                tool.status = 'R'
                tool.save()
            return HttpResponseRedirect('/tool/')
        form = ReturnForm()
    else:
        form = ReturnForm()  # An unbound form

    return render(request, 'Tool/return.html', {'tool': tool, 'form': form})

def pickup_tool(request, pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = PickupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pickup = data['pickup']
            if pickup == True:
                tool.status = 'B'
                tool.save()
                return HttpResponseRedirect('/tool/')
    else:
        form = PickupForm()
    return render(request, 'Tool/pickup_tool.html', {'form' : form})

def return_check(request, pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = CheckReturn(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            returned = data['returned']
            damaged = data['damaged']
            if returned:
                if damaged:
                    tool.status = 'D'
                    tool.save()
                    pm_write(
                        sender=User.objects.get(id=tool.owner.id),
                        recipient=User.objects.get(id=tool.borrower.id),
                        subject='Tool: ' + tool.toolname + ' Damaged',
                        body='The tool you have borrowed has been returned, but the condition has been marked as'
                             + ' damaged.\n'
                             + 'Please get in contact with the owner to make reparations for this damage.\n'
                             + 'The admin has been notified, and MAY suspend your account until this has been resolved')
                else:
                    tool.status = 'A'
                    tool.save()
                return HttpResponseRedirect('/tool/returned/')
    else:
        form = CheckReturn()
    return render(request, 'Tool/return_check.html', {'form' : form})

def pickups(request):
    if request.user.is_authenticated():
        pickup_tool_list = Tool.objects.filter(status='P')
        my_pickup_tool_list = []
        for ptool in pickup_tool_list:
            if ptool.borrower == request.user:
                my_pickup_tool_list.append(ptool)
    return render(request, 'Tool/pickup.html', {'my_pickup_tool_list': my_pickup_tool_list})


class CreateToolView(CreateView):
    model = Tool
    exclude = ['borrows', 'requests']
    success_url = '/tool/'
    img = None

    def form_valid(self, form):
        tool = form.save(commit=False)
        tool.owner = User.objects.get(username=self.request.user.username)
        tool.status = 'U'
        tool.borrows = 0
        tool.requests = 0
        tool.save()
        register_tool_with_user(User.objects.get(username=self.request.user.username), tool.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


def ToolDetail(request, Tool_id):
    tool = Tool.objects.get(id=Tool_id)
    shared = tool.shared
    tool.save()
    return render(request, 'Tool/detail.html', {'tool': tool, 'shared': shared})


class UpdateToolView(UpdateView):
    model = Tool
    #object = Tool.objects.get(self.kwargs['Tool_id'])
    fields = ['shared', 'ownershed']
    #Tool.ownershed = models.ForeignKey(Shed, blank=True, null=True, limit_choices_to=self.request.user.ShareUser.sheds)
    form = UpdateToolForm
    success_url = '/accounts/my_tools/'
    template_name = 'Tool/tool_update_form.html'

    def form_valid(self, form):
        tool = form.save(commit = False)
        tool_owner = tool.owner
        current_user = User.objects.get(username=self.request.user.username)
        if (tool_owner.id == current_user.id) and ((tool.status == ('A')) or (tool.status == ('U'))):
            if tool.shared:
                tool.status = 'A'
            else:
                tool.status = 'U'
            tool.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


class DeleteToolView(DeleteView):
    model = Tool
    success_url = '/tool/'



class DisplayToolView(DetailView):
    model = Tool
    template_name = 'Tool/display.html'

    def get_context_data(self, **kwargs):
        context = super(DisplayToolView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def register_tool_with_user(user, tool_id):
    tool_to_add = Tool.objects.get(id=tool_id)
    user.shareuser.tools.add(tool_to_add)
    return

def MyToolList(request):
    if request.user.is_authenticated():
        query_tool_list = request.user.shareuser.tools.all()
        return render(request, 'share_user/my_tool.html', {'query_tool_list': query_tool_list})
    else:
        return render(request, 'share_user/my_tool.html')

def tool_detail(request, pk):
    tool = Tool.objects.get(id=pk)
    return render(request, 'Tool/display.html', {'tool': tool})