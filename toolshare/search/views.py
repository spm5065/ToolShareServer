from django.shortcuts import render
from Tool.models import Tool
from Shed.models import Shed
# Create your views here.

def search(request):
    if request.method == 'POST':
        searchstr = request.POST['search']
        try:
            list1 = []
            list1.extend(Tool.objects.filter(toolname__contains=searchstr))
        except Tool.DoesNotExist:
            list1 = False
        try:
            list2 = []
            list2.extend(Tool.objects.filter(description__contains=searchstr))
        except Tool.DoesNotExist:
            list2 = False
        if list2:
            if list1:
                for tool in list2:
                    if tool not in list1:
                        list1.append(tool)
            else:
                list1 = list2
        try:
            list3 = []
            list3.extend(Shed.objects.filter(shed_Name__contains=searchstr))
        except Shed.DoesNotExist:
            list3 = False
        try:
            list4 = []
            list4.extend(Shed.objects.filter(description__contains=searchstr))
        except Shed.DoesNotExist:
            list4 = False
        if list4:
            if list3:
                for shed in list4:
                    if shed not in list3:
                        list3.append(shed)
            else:
                list3 = list4
        if (list3 == False) and (list1 == False):
            bool = False
        else:
            bool = True
    return render(request, 'Search/Search.html', {'tool_list': list1, 'shed_list': list3, 'bool': bool})
