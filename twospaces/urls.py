from django.conf.urls import patterns, include, url

main_patterns = patterns('twospaces.conference.views',
  url(r'^$', 'home_redirect', name='home-redirect'),
  url(r'^favicon.ico$', 'favicon', name='favicon'),
  url(r'^([-\w]+)/$', 'conference_home', name='conference-home'),
  url(r'^([-\w]+)/sponsor/$', 'conference_sponsor', name='conference-sponsor'),
)
