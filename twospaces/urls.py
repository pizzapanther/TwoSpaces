from django.conf.urls import patterns, include, url

main_patterns = patterns('twospaces.conference.views',
  url(r'^$', 'home_redirect', name='home-redirect'),
  url(r'^favicon.ico$', 'favicon', name='favicon'),
  url(r'^([-\w]+)/$', 'conference_home', name='conference-home'),
  url(r'^([-\w]+)/sponsor/$', 'conference_sponsor', name='conference-sponsor'),
  url(r'^([-\w]+)/sponsors/$', 'conference_sponsors', name='conference-sponsors'),
  url(r'^([-\w]+)/submit-talk/$', 'conference_submit_talk', name='conference-submit-talk'),
  url(r'^([-\w]+)/submit-talk/success/$', 'conference_submit_talk_success', name='conference-submit-talk-success'),
  
  url(r'^([-\w]+)/proposed-talks/$', 'conference_proposed_talks', name='conference-proposed-talks'),
  
  url(r'^invoice/(\S+)/$', 'invoice', name='conference-invoice'),
)

main_patterns += patterns('',
  url(r'^profile/', include('twospaces.profiles.urls', namespace='profiles', app_name='profiles')),
)
