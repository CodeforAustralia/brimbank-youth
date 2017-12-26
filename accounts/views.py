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
from django.http import JsonResponse

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token
from .models import Profile

def test(request):
    return render(request, "accounts/account_activation_email.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
			
            # Send confirmation email
            current_site = get_current_site(request)
            # message = render_to_string('accounts/account_activation_email.html', {
            message = render_to_string('accounts/drip.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
#            to_email = form.cleaned_data.get('email')
#            to_email = to_email.split(',')
#            to_email = ['devy@codeforaustralia.org']
            to_email = ['dsihaloho@student.unimelb.edu.au']
            sender = form.cleaned_data.get('email')
            send_mail(mail_subject, message, sender, to_email, html_message=message)
			
            # Users are logged in
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'Please wait for the admin to confirm your registration.')
            return redirect('account_activation_sent')
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

# After registering, users can enter their profile
@method_decorator(login_required, name='dispatch')
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
        messages.add_message(request, messages.SUCCESS, 'Your profile has been updated.')
        return redirect('home')
    
def signup_ajax_form(request):
    data = dict()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Users are logged in
            # auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#            messages2 = messages.add_message(request, messages.SUCCESS, 'Please wait for the admin to confirm your registration.')
            
            # Send data to AJAX form
            data['form_is_valid'] = True

            # Send confirmation email
            current_site = get_current_site(request)
            message = render_to_string('accounts/account_activation_email.html', {
            # message = render_to_string('accounts/drip.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = ['dsihaloho@student.unimelb.edu.au']
            sender = form.cleaned_data.get('email')
            send_mail(mail_subject, message, sender, to_email, html_message=message)
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