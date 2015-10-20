from django.conf.urls import include, url

import twospaces.conference.api1_views as conf_v1_views
import twospaces.profiles.api1_views as profile_v1_views
import twospaces.blog.api1_views as blog_v1_views

speakers_v1_urls = [
    url(r'^proposed-talks$',
        conf_v1_views.proposed_talks,
        name="proposed-talks"),
    url(r'^talk/(\d+)$',
        conf_v1_views.talk_detail,
        name="talk-detail"),
    url(r'^submit-talk$',
        conf_v1_views.edit_talk,
        name="submit-talk"),
    url(r'^edit-talk/(\d+)$',
        conf_v1_views.edit_talk,
        name="edit-talk"),
    url(r'^my-talks$',
        conf_v1_views.my_talks,
        name="my-talks"),
    url(r'^schedule$',
        conf_v1_views.schedule,
        name="schedule"),
    url(r'^pyvideo$',
        conf_v1_views.pyvideo,
        name="pyvideo"),
]

users_v1_urls = [
    url(r'^profile/(\S+)$',
        profile_v1_views.user_detail,
        name="user-detail"),
    url(r'^login$',
        profile_v1_views.login_view,
        name="login"),
    url(r'^logout$',
        profile_v1_views.logout_view,
        name="logout"),
    url(r'^sign-up$',
        profile_v1_views.edit_profile,
        name="sign-up"),
    url(r'^my-profile$',
        profile_v1_views.edit_profile,
        name="my-profile"),
    url(r'^my-profile-image$',
        profile_v1_views.profile_image,
        name="my-profile-image"),
    url(r'^verify$',
        profile_v1_views.verify,
        name="verify"),
    url(r'^reset-password$',
        profile_v1_views.start_reset_password,
        name="start-reset-password"),
    url(r'^reset-password-finish$',
        profile_v1_views.finish_reset_password,
        name="finish-reset-password"),
    url(r'^avatar-upload$',
        profile_v1_views.avatar_upload,
        name="avatar-upload"),
]

conf_v1_urls = [
    url(r'^data$',
        conf_v1_views.conf_data,
        name="data"),
    url(r'^sponsors',
        conf_v1_views.sponsor_data,
        name="sponsors"),
    url(r'^attendees',
        conf_v1_views.attendees,
        name="attendees"),
]

blog_v1_urls = [
    url(r'^posts$',
        blog_v1_views.posts,
        name="posts"),
    url(r'^latest$',
        blog_v1_views.latest,
        name="latest"),
    url(r'^post/(\S+)$',
        blog_v1_views.post_detail,
        name="post-detail"),
]

version1_urls = [
    url('^speakers/',
        include(speakers_v1_urls,
                namespace='speakers')),
    url('^users/',
        include(users_v1_urls,
                namespace='users')),
    url('^conferences/',
        include(conf_v1_urls,
                namespace='conferences')),
    url('^blog/',
        include(blog_v1_urls,
                namespace='blog')),
]

urlpatterns = [url('^v1/', include(version1_urls, namespace='v1')),]
