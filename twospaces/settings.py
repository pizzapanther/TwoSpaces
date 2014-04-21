from django.conf import settings

SPONSOR_NOTIFY = getattr(settings, 'TWOSPACES_SPONSOR_NOTIFY', ())
SPEAKER_NOTIFY = getattr(settings, 'TWOSPACES_SPEAKER_NOTIFY', ())
