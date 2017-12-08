from django.shortcuts import render
from django.conf import settings

from twilio.rest import Client
import arrow

def send_sms(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    body = 'Hi Devy. Below is the list of activities that you may be interested in'
    client.messages.create(
            body=body,
            from_=settings.TWILIO_NUMBER,
            to="+61424115157"
    )
    print ('SMS sent')
    return render(request, 'home.html')