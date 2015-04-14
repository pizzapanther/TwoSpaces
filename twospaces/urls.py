from django.conf.urls import include, url

import twospaces.conference.api1_views as conf_v1_views
import twospaces.profiles.api1_views as profile_v1_views

speakers_v1_urls = [
  url(r'^proposed-talks$', conf_v1_views.proposed_talks, name="proposed-talks"),
  url(r'^talk/(\d+)$', conf_v1_views.talk_detail, name="talk-detail"),
  url(r'^submit-talk$', conf_v1_views.edit_talk, name="submit-talk"),
  url(r'^edit-talk/(\d+)$', conf_v1_views.edit_talk, name="edit-talk"),
  url(r'^my-talks$', conf_v1_views.my_talks, name="my-talks"),
]

users_v1_urls = [
  url(r'^profile/(\S+)$', profile_v1_views.user_detail, name="user-detail"),
  url(r'^login$', profile_v1_views.login_view, name="login"),
  url(r'^logout$', profile_v1_views.logout_view, name="logout"),
  url(r'^sign-up$', profile_v1_views.edit_profile, name="sign-up"),
  url(r'^my-profile$', profile_v1_views.edit_profile, name="my-profile"),
  url(r'^verify$', profile_v1_views.verify, name="verify"),
]

conf_v1_urls = [
  url(r'^data$', conf_v1_views.conf_data, name="data"),
]

version1_urls = [
  url('^speakers/', include(speakers_v1_urls, namespace='speakers')),
  url('^users/', include(users_v1_urls, namespace='users')),
  url('^conferences/', include(conf_v1_urls, namespace='conferences')),
]

urlpatterns = [
  url('^v1/', include(version1_urls, namespace='v1')),
]
