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
from django.contrib.auth import views as auth_views

from events import views
from sendsms.views import send_sms, SMSCreateView, EmailCreateView
from activities.views import share_url, bookmark_list, bookmark_activity, ActivityCreateView, ActivityDetailView, ActivityListView, ActivityUpdateView, ActivityDraftDetailView, ActivityDeleteView, ActivityDraftUpdateView, search_events, submit_activity, view_activity_drafts
from accounts import views as accounts_views
from contacts import views as contacts_views

urlpatterns = [
    # Home
    url(r'^$', search_events, name='home'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # social_django
    
    # Accounts
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^account_activation_sent/$', accounts_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        accounts_views.activate, name='activate'),
    url(r'^admin/', admin.site.urls),
    url(r'^edit_profile/$', accounts_views.EnterProfileView.as_view(), name='enter_profile'),
    url(r'^signup_ajax_form/$', accounts_views.signup_ajax_form, name='signup_ajax_form'),
    
    
    # Password management
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
    # Events
    url(r'^events/$', views.events, name='events'),
    url(r'^error/$', views.error, name='error'),
    url(r'^main_search/$', views.search_from_here, name='main_search'),
    
    # Send SMS
    url(r'^sms/$', send_sms, name='send_sms'),
    url(r'^sms_create/(?P<pk>\w+)/$', SMSCreateView.as_view(), name='sms_create'),
    
    # Send Email
    url(r'^email_create/(?P<pk>\w+)/$', EmailCreateView.as_view(), name='email_create'),
    
    # Testing
    url(r'^test_signup_real/$', accounts_views.test_signup_real, name='test_signup_real'),
    url(r'^test_signup/$', accounts_views.test_signup, name='test_signup'),

    url(r'^test_email/$', accounts_views.test, name='test_email'),
    
    # Activities
    url(r'^activity/search/$', search_events, name='search_activity'),
    url(r'^create_activity/$', ActivityCreateView.as_view(), name='create_activity'),
    # url(r'^activity/$', ActivityListView.as_view(), name='activity_list'),
    url(r'^activity/detail/(?P<pk>\d+)/$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^activity/publish/(?P<pk>\d+)/$', ActivityDraftDetailView.as_view(), name='activity_publish'),
    
    url(r'^activity/submit/(?P<pk>\d+)/$', submit_activity, name='submit_activity'),
    url(r'^activity/edit/(?P<pk>\d+)/$', ActivityUpdateView.as_view(), name='edit_activity'),
    url(r'^activity/draft/edit/(?P<pk>\d+)/$', ActivityDraftUpdateView.as_view(), name='edit_draft_activity'),
    url(r'^activity/delete/(?P<pk>\d+)/$', ActivityDeleteView.as_view(), name='delete_activity'),

    url(r'^activity/drafts/$', view_activity_drafts, name='view_activity_drafts'),

    url(r'^activity/bookmark/(?P<pk>\d+)/$', bookmark_activity, name='bookmark_activity'),
    url(r'^activity/bookmarks/$', bookmark_list, name='bookmark_list'),

    # SMS & Email Groups

    # --- SMS contacts ---
    url(r'^sms_contacts/group/$', contacts_views.sms_contact_list, name='sms_contact_list'),
    url(r'^sms_members/create/$', contacts_views.sms_member_create, name='sms_member_create'),
    url(r'^sms_members/(?P<pk>\d+)/update/$', contacts_views.sms_member_update, name='sms_member_update'),
    url(r'^sms_members/(?P<pk>\d+)/delete/$', contacts_views.sms_member_delete, name='sms_member_delete'),

    # --- SMS groups ---
    url(r'^sms_groups/$', contacts_views.sms_group_list, name='sms_group_list'),
    url(r'^sms_groups/create/$', contacts_views.group_create, name='group_create'),
    url(r'^sms_groups/(?P<pk>\d+)/update/$', contacts_views.sms_group_update, name='sms_group_update'),
    url(r'^sms_groups/(?P<pk>\d+)/delete/$', contacts_views.sms_group_delete, name='sms_group_delete'),

    # --- Email groups ---
    url(r'^email_groups/$', contacts_views.email_group_list, name='email_group_list'),
    url(r'^email_groups/create/$', contacts_views.email_group_create, name='email_group_create'),
    url(r'^email_groups/(?P<pk>\d+)/update/$', contacts_views.email_group_update, name='email_group_update'),
    url(r'^email_groups/(?P<pk>\d+)/delete/$', contacts_views.email_group_delete, name='email_group_delete'),

    # --- Email contacts ---
    url(r'^email_contacts/group/$', contacts_views.email_contact_list, name='email_contact_list'),
    url(r'^email_members/create/$', contacts_views.email_member_create, name='email_member_create'),
    url(r'^email_members/(?P<pk>\d+)/update/$', contacts_views.email_member_update, name='email_member_update'),
    url(r'^email_members/(?P<pk>\d+)/delete/$', contacts_views.email_member_delete, name='email_member_delete'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)