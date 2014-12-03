from django.shortcuts import get_object_or_404, render, render_to_response
from Tool.models import Tool
from borrow import forms
from postman.api import pm_write
from django.contrib.auth.models import User
from borrow.models import BorrowRequest

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


def request(request, pk):
    tool = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = forms.RequestForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            borrower = request.user
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            br = BorrowRequest(borrower=borrower, tool=tool, start_date=start_date, end_date=end_date)
            tool.requests += 1
            if tool.status=='A':
                br.approved = True
                tool.borrows += 1
                if tool.ownershed == None:
                    br.approved = False  # Need owner's manual approval so set to false
                    tool.status = 'Q'
                    tool.borrower = borrower
                    tool.save()
                    body = form.cleaned_data['message']
                    message = 'Borrower\'s Custom Message:\n' + body + '\n\n' \
                              'Borrow Period: ' + start_date.strftime('%m/%d/%Y') + ' - ' + end_date.strftime('%m/%d/%Y')+ \
                              '\n' + 'Please either Approve or Reject this request on the top bar under "Tools on Loan" > "Requests"'
                    pm_write(
                        sender=User.objects.get(id=tool.owner.id),
                        recipient=User.objects.get(id=tool.borrower.id),
                        subject='Borrow Request of' + tool.toolname + ' has been denied!',
                        body=message)
                    return HttpResponseRedirect(reverse('tool:detail', args=(pk,)))
                else:
                    tool.status = 'P'
                    tool.borrower=borrower
                    tool.save()
                br.save()
                return HttpResponseRedirect(reverse('tool:detail', args=(pk,)))  # Redirect after POST
            else:
                br.approved = False
    else:
        form = forms.RequestForm()  # An unbound form

    return render(request, 'borrow/request.html', {'tool': tool, 'form': form})
