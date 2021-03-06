from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.messages import constants as messages_const
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from .models import SendSMS, SendEmail
from .forms import SendSMSForm, SendEmailForm
from activities.models import Activity
from accounts.models import Profile
from contacts.models import EmailGroup

from twilio.rest import Client

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of the context."""
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
            # return JsonResponse(form.errors)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class SMSCreateView(AjaxableResponseMixin, CreateView):
    model = SendSMS
    form_class = SendSMSForm
    template_name = 'sendsms/sendsms_form.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        if (profile.sms_limit == 0):
            messages.add_message(self.request, messages.ERROR, 
            'You have exceeded your monthly limit for sending SMS.', extra_tags='danger')
            return redirect('home')
        return super(SMSCreateView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        text_msg = str(self.object.message + '\n' + self.object.activity_list)
        if self.object.recipient_group is not None:
            for group in self.object.recipient_group.all():
                recipient_no_group = group.members.all()
                if recipient_no_group:
                    for member in recipient_no_group:
                        send_sms(text_msg, member.mobile)

        if self.object.recipient_no != '':
            recipient_no_list = self.object.recipient_no.split(',')
            for index, recipient_no in enumerate(recipient_no_list):
                send_sms(text_msg, recipient_no)
                
        messages.add_message(self.request, messages.SUCCESS, 'Your text has been sent')

        # Decrease the limit of text message by 1
        profile = Profile.objects.get(user=self.request.user)
        profile.sms_limit -= 1
        profile.save()
        return reverse('search_activity')
    
    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        activity_pk_list = self.kwargs['pk']
        activity_pk_list = activity_pk_list.split('_')
        activity_url = ''
        for index, pk in enumerate(activity_pk_list):
            activity = Activity.objects.get(pk=pk)
            activity_pk = activity.pk
            name = activity.name
            current_site = get_current_site(self.request)
            domain = current_site.domain
            activity_url_temp = name + ': http://'+ domain +str(reverse('activity_detail', args=[activity_pk]))
            if (activity_url != ''):
                activity_url = str(activity_url + '\n' + activity_url_temp)
            else:
                activity_url = str(activity_url_temp)
        initial['activity_list'] = activity_url
        profile = Profile.objects.get(user=self.request.user)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_list = self.kwargs['pk']
        context['pk_list'] = pk_list
        return context

    def get_form_kwargs(self):
        kwargs = super(SMSCreateView, self).get_form_kwargs()
        kwargs['staff'] = self.request.user
        return kwargs

    
class EmailCreateView(AjaxableResponseMixin, CreateView):
    model = SendEmail
    form_class = SendEmailForm
    template_name = 'sendsms/sendemail_form.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous():
            profile = Profile.objects.get(user=self.request.user)
            if (profile.email_limit == 0):
                messages.add_message(self.request, messages.ERROR, 'You have exceeded your monthly limit for sending email.', extra_tags='danger')
                return redirect('home')
        return super(EmailCreateView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        pk_list = self.kwargs['pk']
        pk_list = pk_list.split('_')
        activities = Activity.objects.filter(pk__in=pk_list)
        current_site = get_current_site(self.request)
        sender_email = self.request.user.email
        staff_name = self.request.user.profile.staff_name
        # msg_html = render_to_string('sendsms/email.html',
        msg_html = render_to_string('sendsms/email_template.html',
                   {'activities': activities,
                   'domain':current_site.domain,
                   'sender': sender_email,
                   'staff_name': staff_name,
                   })

        if self.object.sender:
            sender = self.object.sender
        else:
            sender = 'noreply@youshare.net.au'

        if self.object.recipient_group is not None:
            for group in self.object.recipient_group.all():
                recipient_email_group = group.members.all()
                if recipient_email_group:
                    for member in recipient_email_group:
                        send_email(self.request, 
                                self.object.subject, 
                                self.object.message, 
                                sender,
                                member.email.split(','),
                                msg_html)

        if self.object.recipients != '':
            send_email(self.request, 
                   self.object.subject, 
                   '',
                   sender,
                   self.object.recipients.split(','),
                   msg_html)

        messages.add_message(self.request, messages.SUCCESS, 'Your email has been sent')
        # Decrease the limit of email by 1
        profile = Profile.objects.get(user=self.request.user)
        profile.email_limit -= 1
        profile.save()
        return reverse('search_activity')
    
    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        activity_pk_list = self.kwargs['pk']
        activity_pk_list = activity_pk_list.split('_')
        activity_url = ''
        for index, pk in enumerate(activity_pk_list):
            activity = Activity.objects.get(pk=pk)
            activity_pk = activity.pk
            name = activity.name
            current_site = get_current_site(self.request)
            domain = current_site.domain
            activity_url_temp = name + ': http://'+ domain +str(reverse('activity_detail', args=[activity_pk]))
            if (activity_url != ''):
                activity_url = str(activity_url + '\n' + activity_url_temp)
            else:
                activity_url = str(activity_url_temp)
        initial['activity_list'] = activity_url
        initial['subject'] = 'Some activities you might be interested in'
        profile = Profile.objects.get(user=self.request.user)
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        pk_list = self.kwargs['pk']
        context['pk_list'] = pk_list
        return context

    def get_form_kwargs(self):
        kwargs = super(EmailCreateView, self).get_form_kwargs()
        kwargs['staff'] = self.request.user
        return kwargs
    
def convert_number(number):
    number_temp = ''
    for c in number:
        if c != ' ':
            number_temp = number_temp + c
    number = number_temp
    if (number[0] == '0'):
        number = '+61'+number[1:10]
    return number
    
def send_sms(body, number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    number = convert_number(number)
    client.messages.create(
            body=body,
            from_=settings.TWILIO_NUMBER,
            to=number
    )
    print ('SMS sent')
    
def send_email(request, subject, email_content, sender, recipients, msg_html):
    send_mail(subject, email_content, sender, recipients, html_message=msg_html)
    return render(request, 'home.html')

#def send_sms_old(request):
#    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#    body = 'Hi Devy. Below is the list of activities that you may be interested in'
#    client.messages.create(
#            body=body,
#            from_=settings.TWILIO_NUMBER,
#            to="+61424115157"
#    )
#    print ('SMS sent')
#    return render(request, 'home.html')