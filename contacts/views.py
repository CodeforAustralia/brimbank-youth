from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from copy import deepcopy

from .models import SMSMember, ContactGroup, EmailGroup, EmailMember
from .forms import SMSMemberForm, ContactGroupForm, EmailGroupForm, EmailMemberForm, ActivityListForm
from sendsms.forms import ShareActivitiesEmailForm, ShareActivitiesSMSForm
from sendsms.views import send_email, send_sms
from accounts.models import Profile

import arrow
import csv

@login_required
def sms_group_list(request):
    groups = ContactGroup.objects.all().order_by('name')
    sms_members = SMSMember.objects.all()
    return render(request, 'contacts/sms_group_list.html', {
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
            group = form.save()
            print (group.staff)
            data['form_is_valid'] = True
            groups = EmailGroup.objects.filter(staff=request.user).order_by('name')
            data['html_group_list'] = render_to_string('contacts/includes/partial_group_list.html', {
                'groups': groups,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

# -------------- NEW ---------------------
@login_required
def save_contact_group_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            group = form.save()
            group.staff = request.user
            group.save()
            data['form_is_valid'] = True
            groups = EmailGroup.objects.filter(staff=request.user).order_by('name')
            data['html_group_list'] = render_to_string('contacts/includes/partial_email_group_list.html', {
                'groups': groups,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def save_email_contact_form(request, form, group_pk, template_name):
    data = dict()
    group = EmailGroup.objects.get(pk=group_pk)
    if request.method == 'POST':
        if form.is_valid():
            contact = form.save()
            contact.group = group
            contact.save()
            data['form_is_valid'] = True
            email_members = EmailMember.objects.filter(group=group).order_by('last_name')
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_email_contact_list.html', {
                'email_members': email_members,
            })
        else:
            data['form_is_valid'] = False
    context = {
        'form': form,
        'group_pk': group_pk,
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def email_group_list(request):
    groups = EmailGroup.objects.filter(staff=request.user).order_by('name')
    return render(request, 'contacts/email_group_list.html', {
        'groups': groups,
    })

@login_required
def email_group_create(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST)
    else:
        form = EmailGroupForm()
    return save_contact_group_form(request, form, 'contacts/includes/partial_email_group_create.html')

@login_required
def email_group_update(request, pk):
    group = get_object_or_404(EmailGroup, pk=pk)
    if request.method == 'POST':
        form = EmailGroupForm(request.POST, instance=group)
    else:
        form = EmailGroupForm(instance=group)
    return save_contact_group_form(request, form, 'contacts/includes/partial_email_group_update.html')

@login_required
def email_group_delete(request, pk):
    group = get_object_or_404(EmailGroup, pk=pk)
    data = dict()
    if request.method == 'POST':
        group.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        groups = EmailGroup.objects.filter(staff=request.user).order_by('name')
        data['html_group_list'] = render_to_string('contacts/includes/partial_email_group_list.html', {
            'groups': groups,
        })
    else:
        context = {'group': group}
        data['html_form'] = render_to_string('contacts/includes/partial_email_group_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def group_copy(request, pk):
    group = get_object_or_404(EmailGroup, pk=pk)
    data = dict()
    new_group = deepcopy(group)
    new_group.id = None
    today = arrow.now('Australia/Melbourne')
    new_group.created_time = today
    new_group.save()
    members = EmailMember.objects.filter(group=group)
    for member in members:
        new_member = deepcopy(member)
        new_member.id = None
        new_member.group = new_group
        new_member.save()
    groups = EmailGroup.objects.filter(staff=request.user).order_by('name')
    data['html_group_list'] = render_to_string('contacts/includes/partial_email_group_list.html', {
        'groups': groups,
    })
    return JsonResponse(data)

@login_required
def share_activities(request, pk):
    data = dict()
    group = get_object_or_404(EmailGroup, pk=pk)
    form = ActivityListForm
    context = {
        'form': form,
        'group': group,
    }
    data['html_form'] = render_to_string('contacts/includes/partial_share_activities.html', context, request=request)
    return JsonResponse(data)

def create_html(request, pk, form, template_name):
    data = dict()
    member = get_object_or_404(EmailMember, pk=pk)
    context = {
        'form': form,
        'member': member,
    }
    # data['html_form'] = render_to_string('contacts/includes/partial_share_activities_contacts.html', context, request=request)
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def share_activities_contacts(request, pk):
    form = ShareActivitiesEmailForm
    return create_html(request, pk, form, 'contacts/includes/partial_share_activities_contacts.html')

@login_required
def share_activities_contacts_sms(request, pk):
    form = ShareActivitiesSMSForm
    return create_html(request, pk, form, 'contacts/includes/partial_share_activities_sms.html')

@login_required
def post_shared_activities_contacts(request, pk):
    data = dict()
    member = get_object_or_404(EmailMember, pk=pk)
    if request.method == 'POST':
        form = ShareActivitiesEmailForm(request.POST)
        if form.is_valid():
            activities = form.cleaned_data.get('activity_list')
            current_site = get_current_site(request)
            subject = 'Check these out'
            # message = form.cleaned_data.get('message')
            sender = form.cleaned_data.get('sender')
            staff_name = request.user.profile.staff_name
            # msg_html = render_to_string('sendsms/email.html',
            msg_html = render_to_string('sendsms/email_template.html',
                    {'activities': activities,
                    'domain':current_site.domain,
                    'staff_name': staff_name,
                    'sender': sender
                    })
            send_email(request,subject,'',sender,
                [member.email],
                msg_html)
            data['form_is_valid'] = True
    else:
        form = ShareActivitiesEmailForm()
    context = {
        'form': form,
        'member': member,
    }
    data['html_form'] = render_to_string('contacts/includes/partial_share_activities_contacts.html', context, request=request)
    return JsonResponse(data)

@login_required
def post_shared_activities_sms(request, pk):
    data = dict()
    member = get_object_or_404(EmailMember, pk=pk)
    domain = get_current_site(request).domain
    if request.method == 'POST':
        form = ShareActivitiesSMSForm(request.POST)
        if form.is_valid():
            activities = form.cleaned_data.get('activity_list')
            message = form.cleaned_data.get('message')
            for activity in activities:
                message = str(message + "\n" + activity.name + " http://" + str(domain) + "/activity/detail/" + str(activity.pk) +"/")
            send_sms(message, member.mobile)
            data['form_is_valid'] = True
    else:
        profile = Profile.objects.get(user=request.user)
        if (profile.sms_limit == 0):
            data['limit_exceeded'] = True
        else:
            form = ShareActivitiesSMSForm()
    context = {
        'form': form,
        'member': member,
    }
    data['html_form'] = render_to_string('contacts/includes/partial_share_activities_sms.html', context, request=request)
    return JsonResponse(data)

@login_required
def get_shared_activities_contacts(request, pk):
    data = dict()
    member = get_object_or_404(EmailMember, pk=pk)
    data['email'] = member.email
    data['mobile_no'] = member.mobile
    return JsonResponse(data)

@login_required
def get_shared_activities(request, pk):
    data = dict()
    email_list = []
    mobileno_list = []
    members = EmailMember.objects.filter(group=EmailGroup.objects.get(pk=pk))
    for member in members:
        email_list.append(member.email)
        mobileno_list.append(member.mobile)
    data['email_list'] = email_list
    data['mobileno_list'] = mobileno_list
    return JsonResponse(data)

@login_required
def contact_list(request, pk):
    group = EmailGroup.objects.get(pk=pk)
    email_members = EmailMember.objects.filter(group=group).order_by('last_name')
    return render(request, 'contacts/email_contact_list.html', {
        'email_members': email_members,
        'group_name': group.name,
        'group_pk': pk,
    })

@login_required
def member_create(request, pk):
    group_pk = pk
    if request.method == 'POST':
        form = EmailMemberForm(request.POST)
    else:
        form = EmailMemberForm()
    return save_email_contact_form(request, form, group_pk, 'contacts/includes/partial_email_contact_create.html')

def email_member_update(request, pk):
    email_member = get_object_or_404(EmailMember, pk=pk)
    group_pk = email_member.group.pk
    if request.method == 'POST':
        form = EmailMemberForm(request.POST, instance=email_member)
    else:
        form = EmailMemberForm(instance=email_member)
    return save_email_contact_form(request, form, group_pk, 'contacts/includes/partial_email_contact_update.html')

def email_member_delete(request, pk):
    email_member = get_object_or_404(EmailMember, pk=pk)
    group = email_member.group
    email_member.group.pk
    data = dict()
    if request.method == 'POST':
        email_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        email_members = EmailMember.objects.filter(group=group).order_by('last_name')
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
# -------------- END OF NEW ---------------------

@login_required
def group_create(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST)
    else:
        form = EmailGroupForm()
    return save_form(request, form, 'contacts/includes/partial_group_create.html')

@login_required
def sms_group_update(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk)
    if request.method == 'POST':
        form = ContactGroupForm(request.POST, instance=group)
    else:
        form = ContactGroupForm(instance=group)
    return save_form(request, form, 'contacts/includes/partial_group_update.html')

@login_required
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

@login_required
def save_contact_form(request, form, group_pk, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            # sms_members = SMSMember.objects.all().order_by('group')
            sms_members = SMSMember.objects.filter(group_id=group_pk)
            # sms_members = SMSMember.objects.all()
            data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
                'sms_members': sms_members,
            })
        else:
            data['form_is_valid'] = False
    context = {
        'form': form,
        'test': group_pk, # Comment this later, just testing
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def sms_member_create(request, pk):
    if request.method == 'POST':
        form = SMSMemberForm(request.POST)
    else:
        form = SMSMemberForm()
    return save_contact_form(request, form, pk, 'contacts/includes/partial_contact_create.html')

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
    return save_contact_form(request, form, pk, 'contacts/includes/partial_contact_update.html')

def sms_member_delete(request, pk):
    sms_member = get_object_or_404(SMSMember, pk=pk)
    group_pk = sms_member.group.pk
    data = dict()
    if request.method == 'POST':
        sms_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        # sms_members = SMSMember.objects.all()
        sms_members = SMSMember.objects.filter(group_id=group_pk)
        data['html_sms_member_list'] = render_to_string('contacts/includes/partial_contact_list.html', {
            'sms_members': sms_members,
        })
    else:
        context = {
            'sms_member': sms_member,
            'test': group_pk,
        }
        data['html_form'] = render_to_string('contacts/includes/partial_contact_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def download_contacts(request, pk):
    group = EmailGroup.objects.get(pk=pk)

    if group.staff == request.user:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Contacts"' + group.name + '.csv'

        writer = csv.writer(response)
        writer.writerow(['First name', 'Surname', 'Email address', 'Mobile number', 'Gender', 'Age', 'Language(s) spoken'])

        members = EmailMember.objects.filter(group=group).values_list('first_name', 'last_name', 'email', 'mobile', 'gender', 'age', 'language')
        for member in members:
            writer.writerow(member)
        return response
    
    else:
        messages.add_message(request, messages.ERROR, 'Group member list can only be downloaded by the group creator.', extra_tags='danger')
        return redirect('contact_list', group.pk)