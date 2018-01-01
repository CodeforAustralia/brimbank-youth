from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import SMSMember, ContactGroup
from .forms import SMSMemberForm, ContactGroupForm

# Views for groups
@login_required
def sms_group_list(request):
    groups = ContactGroup.objects.all().order_by('name')
    return render(request, 'contacts/sms_group_list.html', {
        'groups': groups,
    })

# Views for contacts
@login_required
def sms_contact_list(request, group_pk):
    # sms_members = SMSMember.objects.filter(group = group_pk)
    sms_members = SMSMember.objects.all()
    group_id = group_pk
    return render(request, 'contacts/contact_list.html', {
        'sms_members': sms_members,
        'group_id': group_id,
    })

@login_required
def sms_member_list(request):
    sms_members = SMSMember.objects.all()
    groups = ContactGroup.objects.all()
    return render(request, 'contacts/contact_list.html', {
        'sms_members': sms_members,
        'groups': groups,
    })

@login_required
def save_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            groups = ContactGroup.objects.all().order_by('name')
            data['html_group_list'] = render_to_string('contacts/includes/partial_group_list.html', {
                'groups': groups,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def group_create(request):
    if request.method == 'POST':
        form = ContactGroupForm(request.POST)
    else:
        form = ContactGroupForm()
    return save_form(request, form, 'contacts/includes/partial_group_create.html')

@login_required
def sms_group_update(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk)
    if request.method == 'POST':
        form = ContactGroupForm(request.POST, instance=group)
    else:
        form = ContactGroupForm(instance=group)
    return save_form(request, form, 'contacts/includes/partial_group_update.html')

def sms_group_delete(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk)
    data = dict()
    if request.method == 'POST':
        group.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        groups = ContactGroup.objects.all().order_by('name')
        data['html_group_list'] = render_to_string('contacts/includes/partial_group_list.html', {
            'groups': groups
        })
    else:
        context = {'group': group}
        data['html_form'] = render_to_string('contacts/includes/partial_group_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def save_contact_form(request, form, group_id, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sms_members = SMSMember.objects.all()
            # sms_members = SMSMember.objects.filter(group = group_id)
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
                'sms_members': sms_members,
            })
        else:
            data['form_is_valid'] = False
    group_id = group_id
    context = {
        'form': form,
        'group_id': group_id,
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def sms_member_create(request, group_pk):
    if request.method == 'POST':
        form = SMSMemberForm(request.POST)
    else:
        form = SMSMemberForm()
    group_id = group_pk
    return save_contact_form(request, form, group_id, 'contacts/includes/partial_contact_create.html')

def sms_member_update(request, pk):
    sms_member = get_object_or_404(SMSMember, pk=pk)
    if request.method == 'POST':
        form = SMSMemberForm(request.POST, instance=sms_member)
    else:
        form = SMSMemberForm(instance=sms_member)
    group_id = pk
    return save_contact_form(request, form, group_id, 'contacts/includes/partial_contact_update.html')

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