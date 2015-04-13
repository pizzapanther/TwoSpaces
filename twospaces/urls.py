from django.conf.urls import include, url

import twospaces.conference.api1_views as conf_v1_views
import twospaces.profiles.api1_views as profile_v1_views

speakers_v1_urls = [
  url(r'^proposed-talks$', conf_v1_views.proposed_talks, name="proposed-talks"),
  url(r'^talk/(\d+)$', conf_v1_views.talk_detail, name="talk-detail"),
]

users_v1_urls = [
  url(r'^profile/(\S+)$', profile_v1_views.user_detail, name="user-detail"),
]

version1_urls = [
  url('^speakers/', include(speakers_v1_urls, namespace='speakers')),
  url('^users/', include(users_v1_urls, namespace='users')),
]

urlpatterns = [
  url('^v1/', include(version1_urls, namespace='v1')),
]
