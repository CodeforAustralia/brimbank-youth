from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from activities.models import Activity
from sendsms.views import send_email
from .models import Registration
from .forms import RegistrationForm

# Create your views here.
def register(request, pk):
    activity = Activity.objects.get(pk=pk)
    activity_pk = pk
    pk = {'activity_pk': activity_pk}
    if request.method == 'POST':
        form = RegistrationForm(request.POST, **pk)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.activity = activity
            registration.save()
            registration = Registration.objects.get(pk=registration.pk)
            registration_pk = registration.pk
            if activity.space_choice == 'Limited':
                activity.space -= 1
                activity.save()
            # Send confirmation email
            current_site = get_current_site(request)
            domain = current_site.domain
            msg_html = render_to_string('booking/confirmation_email.html',
            {'activity': activity,
            'domain': domain,
            })
            send_email(request, str('Confirmation to '+activity.name), '', 'noreply@youthposter.com', [registration.email], msg_html)
            return redirect('registration_detail', pk=registration_pk)
    else:
        if activity.space_choice == 'Limited' and activity.space <= activity.bookings.count():
            messages.info(request, 'Sorry, this activity is fully booked.')
            return redirect('activity_detail', pk=activity_pk)
        else:
            form = RegistrationForm(**pk)
    return render(request, 'booking/registration_form.html', {
        'form': form,
        'activity': activity,
    })

class RegistrationDetailView(DetailView):
    model = Registration
    template_name = 'booking/registration_confirmation.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        org_activities = Activity.objects.filter(created_by=self.object.activity.created_by).exclude(id=self.object.activity.pk).order_by('name')
        context['org_activities'] = org_activities
        recommended_activities_full = Activity.objects.filter(activity_type=self.object.activity.activity_type).exclude(id=self.object.activity.pk).order_by('name')
        if recommended_activities_full.count() > 1:
            recommended_activities = recommended_activities_full[1:]
        else:
            recommended_activities = recommended_activities_full
        context['recommended_activities'] = recommended_activities
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context['domain'] = domain
        return context