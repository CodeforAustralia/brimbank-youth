from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Activity
from .forms import ActivityForm, ActivitySearchForm
from sendsms.forms import SendSMSForm

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
    
class ActivityDeleteView(DeleteView):
    model = Activity
    success_url = reverse_lazy('activity_search')
    
def search_logic(request, keywords):
    activities = Activity.objects.filter(
    Q(location__istartswith=keywords) | Q(location__iendswith=keywords) | Q(location__icontains=keywords)
    )
    return activities

def search_events(request):
    activities = search_logic(request, '')
    if request.method == 'GET':
        keywords = request.GET.get('location') # 'location' is the name of the input field
        list_of_input_ids=request.GET.getlist('checkboxes')
        str1 = '_'.join(list_of_input_ids)
        search = request.GET.get('search')
        print(list_of_input_ids)
        print(request.GET)
        if search == 'search':
            if keywords:
                activities = search_logic(request, keywords)
        if search == 'share':
            form = SendSMSForm()
#            return render(request, 'sendsms/sendsms_form.html', {'pk': list_of_input_ids, 'form': form})
            kwargs = {'pk': str1}
            return redirect('sms_create', **kwargs)
        activities = show_page_numbers(request, activities)
        return render(request, 'activities/activity_search_result.html', {'activities': activities,})
#        return render(request, 'activities/activity_search_result.html', {'activities': activities,})

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