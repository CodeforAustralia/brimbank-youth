from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
			
            # Send confirmation email
#            current_site = get_current_site(request)
#            message = render_to_string('acc_active_email.html', {
#                'user':user, 
#                'domain':current_site.domain,
#                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                'token': account_activation_token.make_token(user),
#            })
#            mail_subject = 'Activate your account.'
#            to_email = form.cleaned_data.get('email')
#            email = EmailMessage(mail_subject, message, to=[to_email])
#            email.send()
			
            # Users are logged in
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})