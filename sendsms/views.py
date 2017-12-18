from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.messages import constants as messages_const
from django.contrib.sites.shortcuts import get_current_site

from .models import SendSMS, SendEmail
from activities.models import Activity
from .forms import SendSMSForm, SendEmailForm

from twilio.rest import Client

class SMSCreateView(CreateView):
    model = SendSMS
    form_class = SendSMSForm
    
    def get_success_url(self):
        send_sms(self.object.message, self.object.recipient_no)
        messages.add_message(self.request, messages.SUCCESS, 'Your text has been sent')
        return reverse('search_activity')
    
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(CreateView, self).get_initial()
        activity_pk_list = self.kwargs['pk']
        activity_pk_list = activity_pk_list.split('_')
        activity_url = 'Activities you may be interested in:'
        for index, pk in enumerate(activity_pk_list):
            activity = Activity.objects.get(pk=pk)
            activity_pk = activity.pk
            name = activity.name
            current_site = get_current_site(self.request)
            domain = current_site.domain
#            activity_url_temp = name + ' http://localhost:8000'+str(reverse('activity_detail', args=[activity_pk]))
            activity_url_temp = name + ' '+ domain +str(reverse('activity_detail', args=[activity_pk]))
            activity_url = str(activity_url + '\n' + activity_url_temp)
        print(activity_url)
        initial['message'] = activity_url
        return initial
    
class EmailCreateView(CreateView):
    model = SendEmail
    form_class = SendEmailForm
    template_name = 'sendsms/sendemail_form.html'
    
    def get_success_url(self):
        subject = 'Hello Winta!'
        pk_list = self.kwargs['pk']
        pk_list = pk_list.split('_')
        activities = Activity.objects.filter(pk__in=pk_list)
        current_site = get_current_site(self.request)
        msg_html = render_to_string('sendsms/email.html',
                   {'activities': activities,
                   'domain':current_site.domain,
                   }
                                   )
        send_email(self.request, 
                   self.object.subject, 
                   self.object.message, 
                   self.object.sender,
                   self.object.recipients.split(','),
                   msg_html)
        messages.add_message(self.request, messages.SUCCESS, 'Your email has been sent')
        return reverse('search_activity')
    
    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        activity_pk_list = self.kwargs['pk']
        activity_pk_list = activity_pk_list.split('_')
        activity_url = 'Activities you may be interested in:'
        for index, pk in enumerate(activity_pk_list):
            activity = Activity.objects.get(pk=pk)
            activity_pk = activity.pk
            name = activity.name
            current_site = get_current_site(self.request)
            domain = current_site.domain
            activity_url_temp = name + ' '+ domain +str(reverse('activity_detail', args=[activity_pk]))
#            activity_url_temp = name + ' http://localhost:8000'+str(reverse('activity_detail', args=[activity_pk]))
            activity_url = str(activity_url + '\n' + activity_url_temp)
#        print(activity_url)
        initial['message'] = activity_url
        initial['subject'] = 'Activities of the month!!'
        return initial
    
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
#    send_mail(subject, email_content, 'noreply@bottlenose.co', ['devy@codeforaustralia.org'])
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