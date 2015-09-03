from django.conf.urls import include, url

urlpatterns = [
    url(r'^invoice/(\S+)/$',
        'twospaces.conference.views.invoice',
        name='conference-invoice'),
]
