from django.conf.urls import include, url

import twospaces.conference.api1_views as conf_v1_views

speakers_v1_urls = [
  url(r'^proposed-talks$', conf_v1_views.proposed_talks, name="proposed-talks"),
  url(r'^talk/(\d+)$', conf_v1_views.talk_detail, name="talk_detail"),
]

version1_urls = [
  url('^speakers/', include(speakers_v1_urls, namespace='speakers')),
]

urlpatterns = [
  url('^v1/', include(version1_urls, namespace='v1')),
]
