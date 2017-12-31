from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import SMSMember
from .forms import SMSMemberForm

# Create your views here.
@login_required
def sms_member_list(request):
    sms_members = SMSMember.objects.all()
    return render(request, 'contacts/contact_list.html', {'sms_members': sms_members})

@login_required
def save_contact_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sms_members = SMSMember.objects.all()
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
                'sms_members': sms_members
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def sms_member_create(request):
    if request.method == 'POST':
        form = SMSMemberForm(request.POST)
    else:
        form = SMSMemberForm()
    return save_contact_form(request, form, 'contacts/includes/partial_contact_create.html')

def sms_member_update(request, pk):
    sms_member = get_object_or_404(SMSMember, pk=pk)
    if request.method == 'POST':
        form = SMSMemberForm(request.POST, instance=sms_member)
    else:
        form = SMSMemberForm(instance=sms_member)
    return save_contact_form(request, form, 'contacts/includes/partial_contact_update.html')

def sms_member_delete(request, pk):
    sms_member = get_object_or_404(SMSMember, pk=pk)
    data = dict()
    if request.method == 'POST':
        sms_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        sms_members = SMSMember.objects.all()
        data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
            'sms_members': sms_members
        })
    else:
        context = {'sms_member': sms_member}
        data['html_form'] = render_to_string('contacts/includes/partial_contact_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)