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
from django.contrib.sites.shortcuts import get_current_site

import datetime

from .models import Activity, ActivityDraft
from .forms import ActivityForm, ActivitySearchForm, ActivityDraftForm, ShareURLForm
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
    template_name = 'activities/activity_form.html'

    def get_success_url(self):
        messages.info(self.request, 'This is how your activity will appear on YouthPoster. Please check it all carefully before publishing it.')
        return reverse('activity_publish',args=(self.object.id,))
        # self.object.id = pk that is used in ActivityDetailView
        
    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.published = False
        if (object.term == 'Once' and object.activity_date): # set start_date the same as activity_date (for sorting purpose)
            object.start_date = object.activity_date
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.created_by != self.request.user):
            messages.add_message(self.request, messages.ERROR, 'Activity can only be modified by the organiser', extra_tags='danger')
            return redirect('activity_publish', self.object.id )
        return super(ActivityDraftUpdateView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.info(self.request, 'The activity has been updated. You can review the activity before it is published.')
        return reverse('activity_publish',args=(self.object.id,))
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.published = False
        if (object.term == 'Once' and object.activity_date): # set start_date the same as activity_date (for sorting purpose)
            object.start_date = object.activity_date
        object.save()
        return super(ActivityDraftUpdateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ActivityDraftDetailView(DetailView):
    model = ActivityDraft

@login_required
def submit_activity(request, pk):
    draft = ActivityDraft.objects.get(pk=pk)
    error = False
    if not draft.location:
        messages.add_message(request, messages.ERROR, 'Please enter the location.', extra_tags='danger')
        error = True
    if draft.term == 'Once' and not draft.activity_date:
        messages.add_message(request, messages.ERROR, 'Please enter the activity date.', extra_tags='danger')
        error = True
    if draft.term != 'Once' and not draft.start_date:
        messages.add_message(request, messages.ERROR, 'Please enter the start date.', extra_tags='danger')
        error = True
    if draft.term != 'Once' and not draft.end_date:
        messages.add_message(request, messages.ERROR, 'Please enter the end date.', extra_tags='danger')
        error = True
    if error:
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
        if (activity.term == 'Once' and activity.activity_date): # set start_date the same as activity_date (for sorting purpose)
            activity.start_date = draft.activity_date
            activity.save()
        draft.delete()
        messages.add_message(request, messages.SUCCESS, 'The activity has been published.')
        # return render(request, 'activities/activity_detail.html', {
        #     'pk': pk,
        #     'activity': activity,
        # })
        return redirect('home')

class ActivityDetailView(DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['org_activities'] = Activity.objects.filter(created_by=self.object.created_by).exclude(id=self.object.pk).order_by('name')
        recommended_activities_full = Activity.objects.filter(activity_type=self.object.activity_type).exclude(id=self.object.pk).order_by('name')
        if recommended_activities_full.count() > 1:
            recommended_activities = recommended_activities_full[1:]
        else:
            recommended_activities = recommended_activities_full
        context['recommended_activities'] = recommended_activities
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context['domain'] = domain
        return context
    
class ActivityListView(ListView):
    model = Activity
    queryset = Activity.objects.order_by('name')
    paginate_by = 6
    context_object_name = 'activities'

@method_decorator(login_required, name='dispatch')
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.created_by != self.request.user):
            messages.add_message(self.request, messages.ERROR, 'Activity can only be modified by the organiser', extra_tags='danger')
            return redirect('activity_detail', self.object.id )
        return super(ActivityUpdateView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        published = True
#        return reverse('activity_detail',args=(self.object.id,))
        return reverse('activity_detail',kwargs={'pk': self.object.id,})

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Please correct the highlighted fields below.', extra_tags='danger')
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        object = form.save(commit=False)
        if (object.term == 'Once' and object.activity_date): # set start_date the same as activity_date (for sorting purpose)
            object.start_date = object.activity_date
        object.save()
        return super(ActivityUpdateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ActivityDeleteView(DeleteView):
    model = Activity
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.created_by != self.request.user):
            messages.add_message(self.request, messages.ERROR, 'Activity can only be deleted by the organiser', extra_tags='danger')
            return redirect('activity_detail', self.object.id )
        return super(ActivityDeleteView, self).get(request, *args, **kwargs)

def search_logic(request, location_key, name_key, category):
    if category is None:
        category = ''

    activities = Activity.objects.filter(
        Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
        Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key),
        Q(activity_type__istartswith=category) | Q(activity_type__iendswith=category) | Q(activity_type__icontains=category),
    )
    activities = activities.filter(start_date__gte=datetime.date.today())
    activities = activities.order_by('start_date')
    return activities

def search_others(request, location_key, name_key, category):
    if category is None:
        category = ''
        
    other_activities = Activity.objects.filter(
        Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
        Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key)).exclude(
        Q(activity_type__istartswith=category) | Q(activity_type__iendswith=category) | Q(activity_type__icontains=category))
    other_activities = other_activities.filter(start_date__gte=datetime.date.today())
    other_activities = other_activities.order_by('start_date')
    return other_activities

def search_my_activities(request, location_key, name_key, category, mine):
    if mine:
        activities = Activity.objects.filter(created_by=request.user)
        activities = activities.filter(
        Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
        Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key),
        Q(activity_type__istartswith=category) | Q(activity_type__iendswith=category) | Q(activity_type__icontains=category),
        )
        activities = activities.filter(start_date__gte=datetime.date.today()) # filter activities that occur today or later than today
        activities = activities.order_by('start_date')
    else:
        activities = Activity.objects.exclude(created_by=request.user)
        activities = activities.filter(
            Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
            Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key),
            Q(activity_type__istartswith=category) | Q(activity_type__iendswith=category) | Q(activity_type__icontains=category),
        )
        activities = activities.filter(start_date__gte=datetime.date.today())
        activities = activities.order_by('start_date')[0:6]
    return activities

def search_logic_bookmarks(request, location_key, name_key):
    activities = Activity.objects.filter(bookmarked = True, bookmarked_users = request.user)
    activities = activities.filter(
    Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
    Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key)
    )
    return activities

def search_logic_drafts(request, location_key, name_key, category):
    activities = ActivityDraft.objects.filter(
    Q(location__istartswith=location_key) | Q(location__iendswith=location_key) | Q(location__icontains=location_key), 
    Q(name__istartswith=name_key) | Q(name__iendswith=name_key) | Q(name__icontains=name_key),
    Q(activity_type__istartswith=category) | Q(activity_type__iendswith=category) | Q(activity_type__icontains=category),
    )
    return activities

def search_events(request):
    activities = search_logic(request, '', '', '')
    other_activities = None
    not_my_activities = None
    latest_activity = None
    if request.method == 'GET':
        location_key = request.GET.get('location') # 'location' is the name of the input field
        name_key = request.GET.get('name')
        list_of_input_ids=request.GET.getlist('checkboxes')
        str1 = '_'.join(list_of_input_ids)

        search_names=request.GET.getlist('search_name')
        category = request.GET.get('category')
        search = request.GET.get('search')

        if name_key is None:
            name_key = ''
        if location_key is None:
            location_key =''
        if category is None:
            category =''

        if request.user.is_anonymous():
            activities = search_logic(request, location_key, name_key, category)
            other_activities = search_others(request, location_key, name_key, category)

        # if request.user.is_anonymous() == False:
        if not request.user.is_anonymous():
            activities = search_my_activities(request, location_key, name_key, category, True)
            not_my_activities = search_my_activities(request, location_key, name_key, category, False)
            # Display the latest_activity (for the most recent published activity)
            staff_activities = Activity.objects.filter(created_by=request.user)
            if staff_activities:
                latest_activity = staff_activities.filter(created_time__isnull=False).latest('created_time')

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

        url = "&name=" + name_key + "&location=" + location_key + "&category=" + category + "&search=search"

        # Get domain for each activity (to be populated in the share button)
        current_site = get_current_site(request)
        domain = current_site.domain

        return render(request, 'activities/activity_search_result.html', {
                      'other_activities': other_activities,
                      'not_my_activities': not_my_activities,
                      'activities': activities,
                      'latest_activity': latest_activity,
                      'name': name_key,
                      'url': url,
                      'domain': domain
                      })

def show_page_numbers(request, result):
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 9)

    try:
        search_result = paginator.page(page)
    except PageNotAnInteger:
        search_result = paginator.page(1) # fallback to the first page
    except EmptyPage:
        # probably the user tried to add a page number in the url, so we fallback to the last page
        search_result = paginator.page(paginator.num_pages)
    return search_result

@login_required
def view_activity_drafts(request):
    activity_drafts = search_logic_drafts(request, '', '', '')
    if request.method == 'GET':
        location_key = request.GET.get('location') # 'location' is the name of the input field
        name_key = request.GET.get('name')
        list_of_input_ids=request.GET.getlist('checkboxes')
        category = request.GET.get('category')
        # str1 = '_'.join(list_of_input_ids)
        if location_key or name_key or category:
            activity_drafts = search_logic_drafts(request, location_key, name_key, category)
        activity_drafts = show_page_numbers(request, activity_drafts)

        # Also display bookmarked activities
        bookmarks = Activity.objects.filter(bookmarked = True, bookmarked_users = request.user)

        return render(request, 'activities/activitydraft_search_result.html', {
                'activities': activity_drafts,
                'bookmarks': bookmarks,
                })

def bookmark_activity(request, pk):
    activity = Activity.objects.get(pk=pk)
    if (activity.bookmarked):
        activity.bookmarked = False
        activity.bookmarked_users.remove(request.user)
    else:
        activity.bookmarked = True
        activity.bookmarked_users.add(request.user)
    activity.save()
    # new_user = activity.bookmarked_users.get(pk=request.user.pk)
    return HttpResponse('Bookmark test')

@login_required
def bookmark_list(request):
    activities = Activity.objects.filter(bookmarked = True).filter(bookmarked_users=request.user)
    if request.method == 'GET':
        location_key = request.GET.get('location') # 'location' is the name of the input field
        name_key = request.GET.get('name')
        list_of_input_ids=request.GET.getlist('checkboxes')
        str1 = '_'.join(list_of_input_ids)
        search = request.GET.get('search')
        if search == 'search':
            if location_key or name_key:
                activities = search_logic_bookmarks(request, location_key, name_key)
                activities.filter(bookmarked = True)
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
        return render(request, 'activities/activity_bookmarks_list.html', {'activities': activities,})

def share_url(request):
    form = ShareURLForm()
    data = dict()
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string('activities/includes/partial_share_url.html', context, request=request)
    return JsonResponse(data)
