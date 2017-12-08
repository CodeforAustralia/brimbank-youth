from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponse

from .models import Activity
from .forms import ActivityForm

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