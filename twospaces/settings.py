from django.conf import settings

SPONSOR_NOTIFY = getattr(settings, 'TWOSPACES_SPONSOR_NOTIFY', ())
SPEAKER_NOTIFY = getattr(settings, 'TWOSPACES_SPEAKER_NOTIFY', ())

SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'localhost')
SITE_PROTOCOL = getattr(settings, 'SITE_PROTOCOL', 'http')
