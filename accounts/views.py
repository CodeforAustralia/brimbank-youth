import time

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.http import JsonResponse, HttpResponse
from django.core.files import File

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token
from .models import Profile, AdminEmail

from .tasks import print_something

from activities.views import search_logic, show_page_numbers
from activities.models import Activity
from contacts.models import EmailMember, EmailGroup

import csv

@login_required
def bulk_upload_contacts(request):
    path = 'bulk_upload/contacts.csv'
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            member = EmailMember()
            member.group = EmailGroup.objects.get(name=row[0])
            member.first_name=row[1]
            member.last_name=row[2]
            member.email=row[3]
            member.gender=row[4]
            member.mobile=row[5]
            member.age=row[6]
            member.language=row[7]
            member.save()
        f.close()
    members = EmailMember.objects.all()
    for member in members:
        print(member.mobile)
    return HttpResponse("Success uploading contacts")

@login_required
def bulk_upload_activities(request):
    path = 'bulk_upload/activities.csv'
    with open(path, encoding="latin-1") as f:
        reader = csv.reader(f)
        for row in reader:
            activity = Activity()
            activity.name = row[0]
            activity.activity_type=row[1]
            activity.term=row[2]
            activity.location=row[3]
            activity.suburb=row[4]
            activity.postcode=row[5]
            activity.organiser=row[6]
            activity.contact_number=row[7]
            activity.description=row[8]
            activity.activity_date=row[9]
            activity.start_date=row[10]
            activity.end_date=row[11]
            activity.start_time=row[13]
            activity.end_time=row[14]
            activity.created_by = User.objects.get(username=row[15])
                    
            # Image Upload
            if row[16] != '':
                file_dir = 'bulk_upload/images/' + row[16]
                image = open(file_dir, 'rb')
                image_file = File(image)
                activity.activity_img.save(row[16], image_file)
            # Flyer Upload
            if row[17] != '':
                file_dir = 'bulk_upload/flyers/' + row[17]
                flyer = open(file_dir, 'rb')
                flyer_file = File(flyer)
                activity.flyer.save(row[17], flyer_file)

            activity.min_age = row[18]
            activity.max_age = row[19]
            activity.background = row[20]
            activity.living_duration = row[21]
            activity.gender = row[22]
            if row[23] != '':
                activity.cost = row[23]
            if row[24] != '':
                activity.space = row[24]
            activity.cost_choice = row[25]
            activity.space_choice = row[26]
            activity.save()
        f.close()
    return HttpResponse("Success uploading activities.")

def test(request):
    return render(request, "accounts/account_activation_email.html")

def testing(request):
    print_something()
    return HttpResponse("task will be executed in 5 seconds")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone = form.cleaned_data.get('phone')
            user.is_active = False
            user.save()
			
            # Send confirmation email
            current_site = get_current_site(request)
            # message = render_to_string('accounts/account_activation_email.html', {
            message = render_to_string('accounts/welcome.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            # to_email = ['dsihaloho@student.unimelb.edu.au']
            to_email = ['devys@brimbank.vic.gov.au']
            sender = form.cleaned_data.get('email')
            send_mail(mail_subject, message, sender, to_email, html_message=message)
			
            # Users are logged in
            # auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'Please wait for the admin to confirm your registration.')
            activities = search_logic(request, '', '', '')
            activities = show_page_numbers(request, activities)
            user_register = True
            return render(request, 'activities/activity_search_result.html', {'activities': activities,
                                                                            'user_register': user_register,})
            # return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
#    return render(request, 'base.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.add_message(request, messages.SUCCESS, 'Congrats! The account has been activated.')
        return redirect('home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')
    
def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

# @method_decorator(login_required, name='dispatch')
class EnterProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/enter_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        messages.add_message(self.request, messages.SUCCESS, 'Your profile has been updated.')
        return redirect('home')

def create_profile(request, pk):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.profile.organisation_name = form.cleaned_data.get('organisation_name')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.web_address = form.cleaned_data.get('web_address')
            user.profile.staff_name = form.cleaned_data.get('staff_name')
            user.profile.role = form.cleaned_data.get('role')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.description = form.cleaned_data.get('description')
            user.is_active = False
            user.save()

            # Send confirmation email
            current_site = get_current_site(request)
            # message = render_to_string('accounts/welcome.html', {
            message = render_to_string('accounts/activation_request.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = '[YouShare] Login request'
            admin_email = AdminEmail.objects.get(role='admin').email
            to_email = [admin_email]
            # to_email = ['devy.f.sihaloho@gmail.com']
            sender = user.email
            send_mail(mail_subject, message, sender, to_email, html_message=message)
            return redirect('account_activation_sent')
    else:
        form = ProfileForm()
    return render(request, 'accounts/enter_profile.html', {'form': form})

def signup_ajax_form(request):
    data = dict()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        if form.is_valid():
            data['no_progress_display'] = False
            # user = form.save(commit=False)
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.is_active = False
            user.save()

            # Send data to AJAX form
            data['form_is_valid'] = True
            data['user_pk'] = user.pk

        else:
            data['no_progress_display'] = True
            data['form_is_valid'] = False
    else:
        form = SignUpForm()
        
    context = {'form': form}
    data['html_form'] = render_to_string('includes/partial_signup.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def send_progress(data):
    data['no_progress_display'] = True
    return JsonResponse(data)
    
def test_signup(request):
    data = dict()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            users = User.objects.all()
            data['html_book_list'] = render_to_string('includes/partial_user.html', {
                'users': users
            })
        else:
            data['form_is_valid'] = False
    else:
        form = SignUpForm()
        
    context = {'form': form}
    data['html_form'] = render_to_string('includes/partial_signup.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def test_signup_real(request):
    users = User.objects.all()
    return render(request, 'test_signup.html', {'users': users})

def privacy_page(request):
    return render(request, 'disclaimer-privacy.html')

def about_page(request):
    return render(request, 'about.html')