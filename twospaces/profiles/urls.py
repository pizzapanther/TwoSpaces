from django.conf.urls import patterns, include, url

urlpatterns = patterns('twospaces.profiles.views',
  url(r'^signup/$', 'signup', name='signup'),
  url(r'^login/$', 'login_view', name='login'),
  url(r'^logout/$', 'logout_view', name='logout'),
  url(r'^edit/$', 'profile', name='profile'),
  url(r'^speaker-info/$', 'speaker_info', name='speaker-info'),
  url(r'^verify/$', 'email_verify', name='verify'),
  
  url(r'^forgot/$', 'forgot', name='forgot'),
  url(r'^reset/$', 'reset', name='reset'),
  
  url(r'^(\S+)$', 'public_profile', name='public-profile'),
)
