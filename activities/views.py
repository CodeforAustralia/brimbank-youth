from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Activity
from .forms import ActivityForm, ActivitySearchForm

activities = []

# Create your views here.
class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm

    def get_success_url(self):
        return reverse('activity_detail',args=(self.object.id,))
        # self.object.id = pk that is used in ActivityDetailView
    
class ActivityDetailView(DetailView):
    model = Activity
    
class ActivityListView(ListView):
    model = Activity
    paginate_by = 6
    context_object_name = 'activities'
    
class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    
    def get_success_url(self):
        return reverse('activity_detail',args=(self.object.id,))
    
def search_logic(request, keywords):
    activities = Activity.objects.filter(
    Q(location__istartswith=keywords) | Q(location__iendswith=keywords) | Q(location__icontains=keywords)
    )
    return activities

def search_events(request):
    keywords = request.GET.get('location') # 'location' is the name of the input field
    if keywords:
        activities = search_logic(request, keywords)
    else:
        activities = search_logic(request, '')
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