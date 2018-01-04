from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from .models import SMSMember, ContactGroup, EmailGroup, EmailMember
from .forms import SMSMemberForm, ContactGroupForm, EmailGroupForm, EmailMemberForm

@login_required
def sms_group_list(request):
    groups = ContactGroup.objects.all().order_by('name')
    sms_members = SMSMember.objects.all()
    return render(request, 'contacts/sms_group_list.html', {
        'groups': groups,
        'sms_members': sms_members,
    })

@login_required
def email_group_list(request):
    groups = EmailGroup.objects.all().order_by('name')
    sms_members = EmailMember.objects.all()
    return render(request, 'contacts/email_group_list.html', {
        'groups': groups,
        'sms_members': sms_members,
    })

# Views for contacts
@login_required
def sms_contact_list(request):
    # sms_members = SMSMember.objects.filter(group = group_pk)
    sms_members = SMSMember.objects.all().order_by('-group')
    return render(request, 'contacts/contact_list.html', {
        'sms_members': sms_members,
    })

@login_required
def email_contact_list(request):
    email_members = EmailMember.objects.all().order_by('-group')
    return render(request, 'contacts/email_contact_list.html', {
        'email_members': email_members,
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
            sms_members = SMSMember.objects.all()
            data['html_group_list'] = render_to_string('contacts/includes/partial_group_list.html', {
                'groups': groups,
                'sms_members': sms_members,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def save_contact_group_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            groups = EmailGroup.objects.all().order_by('name')
            sms_members = SMSMember.objects.all()
            data['html_group_list'] = render_to_string('contacts/includes/partial_email_group_list.html', {
                'groups': groups,
                'sms_members': sms_members,
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
def email_group_create(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST)
    else:
        form = EmailGroupForm()
    return save_contact_group_form(request, form, 'contacts/includes/partial_email_group_create.html')

@login_required
def sms_group_update(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk)
    if request.method == 'POST':
        form = ContactGroupForm(request.POST, instance=group)
    else:
        form = ContactGroupForm(instance=group)
    return save_form(request, form, 'contacts/includes/partial_group_update.html')

@login_required
def email_group_update(request, pk):
    group = get_object_or_404(EmailGroup, pk=pk)
    if request.method == 'POST':
        form = EmailGroupForm(request.POST, instance=group)
    else:
        form = EmailGroupForm(instance=group)
    return save_contact_group_form(request, form, 'contacts/includes/partial_email_group_update.html')

def sms_group_delete(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk)
    data = dict()
    if request.method == 'POST':
        group.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        groups = ContactGroup.objects.all().order_by('name')
        sms_members = SMSMember.objects.all()
        data['html_group_list'] = render_to_string('contacts/includes/partial_group_list.html', {
            'groups': groups,
            'sms_members': sms_members,
        })
    else:
        context = {'group': group}
        data['html_form'] = render_to_string('contacts/includes/partial_group_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def email_group_delete(request, pk):
    group = get_object_or_404(EmailGroup, pk=pk)
    data = dict()
    if request.method == 'POST':
        group.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        groups = EmailGroup.objects.all().order_by('name')
        sms_members = SMSMember.objects.all()
        data['html_group_list'] = render_to_string('contacts/includes/partial_email_group_list.html', {
            'groups': groups,
            'sms_members': sms_members,
        })
    else:
        context = {'group': group}
        data['html_form'] = render_to_string('contacts/includes/partial_email_group_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def save_contact_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sms_members = SMSMember.objects.all().order_by('group')
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
                'sms_members': sms_members,
            })
        else:
            data['form_is_valid'] = False
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def save_email_contact_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            email_members = EmailMember.objects.all().order_by('-group')
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_email_contact_list.html', {
                'email_members': email_members,
            })
        else:
            data['form_is_valid'] = False
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def sms_member_create(request):
    if request.method == 'POST':
        form = SMSMemberForm(request.POST)
    else:
        form = SMSMemberForm()
    return save_contact_form(request, form, 'contacts/includes/partial_contact_create.html')

@login_required
def email_member_create(request):
    if request.method == 'POST':
        form = EmailMemberForm(request.POST)
    else:
        form = EmailMemberForm()
    return save_email_contact_form(request, form, 'contacts/includes/partial_email_contact_create.html')

def sms_member_update(request, pk):
    sms_member = get_object_or_404(SMSMember, pk=pk)
    if request.method == 'POST':
        form = SMSMemberForm(request.POST, instance=sms_member)
    else:
        form = SMSMemberForm(instance=sms_member)
    return save_contact_form(request, form, 'contacts/includes/partial_contact_update.html')

def email_member_update(request, pk):
    email_member = get_object_or_404(EmailMember, pk=pk)
    if request.method == 'POST':
        form = EmailMemberForm(request.POST, instance=email_member)
    else:
        form = EmailMemberForm(instance=email_member)
    return save_email_contact_form(request, form, 'contacts/includes/partial_email_contact_update.html')

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

def email_member_delete(request, pk):
    email_member = get_object_or_404(EmailMember, pk=pk)
    data = dict()
    if request.method == 'POST':
        email_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        email_members = EmailMember.objects.all()
        data['html_sms_member_list'] = render_to_string('contacts/includes/partial_email_contact_list.html', {
            'email_members': email_members
        })
    else:
        context = {'email_member': email_member}
        data['html_form'] = render_to_string('contacts/includes/partial_email_contact_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)