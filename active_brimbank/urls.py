"""active_brimbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from events import views
from sendsms import views as SMSViews
from activities.views import ActivityCreateView, ActivityDetailView, ActivityListView, ActivityUpdateView, search_events

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/$', views.events, name='events'),
    url(r'^login/$', views.login, name='login'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # social_django
    url(r'^admin/', admin.site.urls),
    url(r'^error/$', views.error, name='error'),
    url(r'^main_search/$', views.search_from_here, name='main_search'),
    url(r'^sms/$', SMSViews.send_sms, name='send_sms'),
    url(r'^create_activity/$', ActivityCreateView.as_view(), name='create_activity'),
    url(r'^activity/$', ActivityListView.as_view(), name='activity_list'),
    url(r'^activity/detail/(?P<pk>\d+)/$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^activity/search/$', search_events, name='search_activity'),
    url(r'^activity/edit/(?P<pk>\d+)/$', ActivityUpdateView.as_view(), name='edit_activity'),
    url(r'^activity_search/$', search_events, name='activity_search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)