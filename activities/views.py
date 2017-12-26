from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants as messages_const
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .models import Activity, ActivityDraft
from .forms import ActivityForm, ActivitySearchForm, ActivityDraftForm
from sendsms.forms import SendSMSForm, SendEmailForm

activities = []

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ActivityCreateView(CreateView):
    model = ActivityDraft
    form_class = ActivityDraftForm

    def get_success_url(self):
        messages.info(self.request, 'The activity has been saved. You can review the activity before it is published.')
        return reverse('activity_publish',args=(self.object.id,))
        # self.object.id = pk that is used in ActivityDetailView
        
    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.published = False
        object.save()
        return super(ActivityCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Please correct the highlighted fields below.', extra_tags='danger')
        response = super().form_invalid(form)
        return response
    
@method_decorator(login_required, name='dispatch')
class ActivityDraftUpdateView(UpdateView):
    model = ActivityDraft
    form_class = ActivityDraftForm
    
    def get_success_url(self):
        messages.info(self.request, 'The activity has been updated. You can review the activity before it is published.')
        return reverse('activity_publish',args=(self.object.id,))
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.published = False
        object.save()
        return super(ActivityDraftUpdateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ActivityDraftDetailView(DetailView):
    model = ActivityDraft

@login_required
def submit_activity(request, pk):
    draft = ActivityDraft.objects.get(pk=pk)
    if draft.organiser == None:
        messages.add_message(request, messages.ERROR, 'Please enter the organiser information.', extra_tags='danger')
        form = ActivityDraftForm(initial=model_to_dict(draft))
        kwargs = {'pk': draft.pk}
        return redirect('edit_draft_activity', **kwargs)
    else:
        activity = Activity(pk=None, 
                            name=draft.name, activity_type=draft.activity_type,
                            term=draft.term,
                            location=draft.location,
                            organiser=draft.organiser,
                            contact_number=draft.contact_number,
                            description = draft.description,
                            activity_date = draft.activity_date,
                            start_date = draft.start_date,
                            activity_day = draft.activity_day,
                            start_time = draft.start_time,
                            end_time = draft.end_time,
                            activity_img = draft.activity_img,
                            flyer = draft.flyer,
                            min_age = draft.min_age,
                            max_age = draft.max_age,
                            background = draft.background,
                            living_duration = draft.living_duration,
                            gender = draft.gender,
                            cost = draft.cost,
                            space = draft.space,
                            cost_choice = draft.cost_choice,
                            space_choice = draft.space_choice,
                            listing_privacy = draft.listing_privacy,
                            created_by = draft.created_by,
                            published = True,
                           )
        activity.save()
        draft.delete()
    #    return render(request, 'activities/activitydraft_detail.html', {
    #        'pk': pk,
    #    })
        return render(request, 'activities/activity_detail.html', {
            'pk': pk,
            'activity': activity,
        })

class ActivityDetailView(DetailView):
    model = Activity
    
class ActivityListView(ListView):
    model = Activity
    queryset = Activity.objects.order_by('name')
    paginate_by = 6
    context_object_name = 'activities'

@method_decorator(login_required, name='dispatch')
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activitydraft_form.html'
    
    def get_success_url(self):
        published = True
#        return reverse('activity_detail',args=(self.object.id,))
        return reverse('activity_detail',kwargs={'pk': self.object.id,})

@method_decorator(login_required, name='dispatch')
class ActivityDeleteView(DeleteView):
    model = Activity
    success_url = reverse_lazy('home')

def search_logic(request, location_key, name_key):
    activities = Activity.objects.filter(
    Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key)
    )
    return activities

def search_events(request):
    activities = search_logic(request, '', '')
    if request.method == 'GET':
        location_key = request.GET.get('location') # 'location' is the name of the input field
        name_key = request.GET.get('name')
        list_of_input_ids=request.GET.getlist('checkboxes')
        str1 = '_'.join(list_of_input_ids)
        search = request.GET.get('search')
        print('list of checkbox: ', list_of_input_ids)
        print('request.get: ', request.GET)
        if search == 'search':
            if location_key or name_key:
                activities = search_logic(request, location_key, name_key)
        if str1 != '':
            kwargs = {'pk': str1}
            if search == 'share':
                form = SendSMSForm()
                return redirect('sms_create', **kwargs)
            if search == 'email':
                form = SendEmailForm()
                return redirect('email_create', **kwargs)
        if (str1 == '' and search == 'share') or (str1 == '' and search == 'email'):
            messages.add_message(request, messages.ERROR, 'Please select at least one activity.', extra_tags='danger')
        activities = show_page_numbers(request, activities)
        return render(request, 'activities/activity_search_result.html', {'activities': activities,})

def show_page_numbers(request, result):
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 6)

    try:
        search_result = paginator.page(page)
    except PageNotAnInteger:
        search_result = paginator.page(1) # fallback to the first page
    except EmptyPage:
        # probably the user tried to add a page number in the url, so we fallback to the last page
        search_result = paginator.page(paginator.num_pages)
    return search_result
