import datetime

from django.db import models
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils import timezone

from twospaces.settings import SPONSOR_NOTIFY, SPEAKER_NOTIFY, SITE_DOMAIN, SITE_PROTOCOL


class ActiveManager(models.Manager):

  def get_queryset(self):
    return super(ActiveManager, self).get_queryset().filter(active=True)


class Conference(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField()

  start = models.DateField()
  end = models.DateField()

  registration_open = models.DateTimeField()
  registration_closed = models.DateTimeField()

  cfp_open = models.DateTimeField("Call for Proposals Open",
                                  blank=True,
                                  null=True)
  cfp_closed = models.DateTimeField("Call for Proposals Closed",
                                    blank=True,
                                    null=True)

  active = models.BooleanField()

  objects = models.Manager()
  live = ActiveManager()

  class Meta:
    ordering = ('-start',)

  def __str__(self):
    return self.name

  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "name__icontains", "slug__icontains")

  def cfp_is_closed(self):
    return cfp_is_closed(self.cfp_open, self.cfp_closed)


def cfp_is_closed(start, end):
  now = timezone.now()

  closed = False
  if start and now < start:
    closed = True

  elif end and now > end:
    closed = True

  return closed


class SponsorshipLevel(models.Model):
  conference = models.ForeignKey(Conference)

  name = models.CharField(max_length=100)
  cost = models.PositiveIntegerField()
  description = models.TextField(blank=True)

  order = models.IntegerField(default=0)

  class Meta:
    ordering = ("order",)

  def __str__(self):
    return '{} {}'.format(self.name, self.conference.slug)

  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "name__icontains")

  def sponsors(self):
    return self.sponsor_set.filter(active=True).order_by('?')


class Sponsor(models.Model):
  name = models.CharField(max_length=100)
  url = models.URLField('URL')
  description = models.TextField(blank=True)

  contact_name = models.CharField(max_length=100, blank=True, null=True)
  contact_phone = models.CharField(max_length=100, blank=True, null=True)
  contact_email = models.EmailField(blank=True, null=True)

  level = models.ForeignKey(SponsorshipLevel)

  active = models.BooleanField()

  logo = models.ImageField(upload_to="sponsor_logos/%Y-%m/",
                           blank=True,
                           null=True)

  def __str__(self):
    return self.name

  def link(self):
    return '<a href="{}" target="_blank">Webpage &raquo;</a>'.format(self.url)

  link.allow_tags = True

  def notify(self):
    if SPONSOR_NOTIFY:
      c = {'sponsor': self}

      slug = self.level.conference.slug
      text_templates = (
          'conference/{}/sponsor-notify.email.txt'.format(slug),
          'conference/sponsor-notify.email.txt')
      html_templates = (
          'conference/{}/sponsor-notify.email.html'.format(slug),
          'conference/sponsor-notify.email.html')

      text = render_to_string(text_templates, c)
      html = render_to_string(html_templates, c)

      msg = EmailMultiAlternatives('New Sponsor', text,
                                   settings.DEFAULT_FROM_EMAIL, SPONSOR_NOTIFY)
      msg.attach_alternative(html, "text/html")
      msg.send()


class Room(models.Model):
  conference = models.ForeignKey(Conference)
  name = models.CharField(max_length=100)
  sorder = models.IntegerField('Order')

  def __str__(self):
    return '{} - {}'.format(self.name, self.conference.slug)

  class Meta:
    ordering = ('sorder',)

  def session_query(self, day):
    return Session.objects.filter(
        conference=self.conference,
        start__year=day.year,
        start__month=day.month,
        start__day=day.day,
        status='accepted',)

  def has_sessions(self, day):
    query = self.session_query(day)
    query = query.filter(room=self)
    return query.exclude(start__isnull=True).order_by('start').count() > 0

  def sessions(self, day):
    query = self.session_query(day)
    query = query.filter(Q(room=self) | Q(all_rooms=True))
    return query.exclude(start__isnull=True).order_by('start').select_related()


SESSION_TYPES = (
    ('lightning', 'Lightning Talk (5 Minutes)'),
    ('talk-short', 'Short Talk (20 Minutes)'),
    ('talk-long', 'Talk (50 Minutes)'), ('tutorial', 'Tutorial (3 Hours)'),
    ('non-talk', 'Non Talk'),)

SESSION_LENGTH = {
    'lightning': 5,
    'talk-short': 20,
    'talk-long': 50,
    'tutorial': 180,
}

SESSION_STATUS = (
    ('submitted', 'Submitted'), ('maybe', 'Maybe'), ('accepted', 'Accepted'),
    ('declined', 'Declined'),)

SESSION_LEVELS = (
    ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),)


class Session(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  conference = models.ForeignKey(Conference)

  room = models.ForeignKey(Room, blank=True, null=True)
  all_rooms = models.BooleanField(default=False)
  video = models.BooleanField('Make recording', default=True)

  name = models.CharField('Title of Talk', max_length=100)
  description = models.TextField()
  slides = models.URLField('URL To Presentation', blank=True, null=True)
  video = models.URLField('URL To Video', blank=True, null=True)

  stype = models.CharField('Session Type', max_length=25, choices=SESSION_TYPES)
  level = models.CharField('Audience Level',
                           max_length=25,
                           choices=SESSION_LEVELS)

  status = models.CharField(max_length=25,
                            choices=SESSION_STATUS,
                            default='submitted')

  start = models.DateTimeField(blank=True, null=True)
  duration = models.IntegerField(blank=True,
                                 null=True,
                                 help_text="Time in Minutes")

  special_requirements = models.TextField(
      blank=True,
      null=True,
      help_text=
      "If you require any special equipment or materials, please let us know here.")

  def __str__(self):
    return self.name

  def set_duration(self):
    self.duration = SESSION_LENGTH[self.stype]

  class Meta:
    ordering = ("start",)

  def email(self):
    return self.user.email

  def full_name(self):
    return u'{self.user.first_name} {self.user.last_name}'.format(self=self)

  def send_submitted(self, request, conf):
    subject = "Talk Submission - {} - {}".format(self.user.__str__(), conf)
    message = render_to_string('conference/email.talk-submission.txt',
                               {'request': request,
                                'session': self})
    send_mail(subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              SPEAKER_NOTIFY,
              fail_silently=False)

  def admin_link(self):
    return '{}://{}/admin/conference/session/{}/'.format(SITE_PROTOCOL,
                                                         SITE_DOMAIN, self.id)

  def user_link(self):
    return '{}://{}/admin/profiles/user/{}/'.format(SITE_PROTOCOL, SITE_DOMAIN,
                                                    self.user.id)

  def end(self):
    return self.start + datetime.timedelta(minutes=self.duration)

  def json_type(self):
    if self.stype.startswith('talk'):
      return 'talk'

    elif self.stype == 'non-talk':
      return 'free-form'

    return self.stype

  @staticmethod
  def schedule(conference, day):
    return Session.objects.filter(
        conference=conference,
        start__year=day.year,
        start__month=day.month,
        start__day=day.day,
        status='accepted',).exclude(start__isnull=True).order_by(
            'start', 'room').select_related()


class Invoice(models.Model):
  to = models.EmailField()
  key = models.CharField(max_length=50, unique=True)
  name = models.CharField('Transaction Name', max_length=255)
  subject = models.CharField(max_length=255)
  text = models.TextField(
      default="Follow the link below to complete your sponsorship transaction.",
      help_text="Link will be generated by the invoice system.")

  amount = models.DecimalField(max_digits=9, decimal_places=2)

  sent = models.DateTimeField(blank=True, null=True)

  stripe_token = models.CharField(max_length=255, blank=True, null=True)
  stripe_charge = models.CharField(max_length=255, blank=True, null=True)

  paid_on = models.DateTimeField(blank=True, null=True)

  class Meta:
    ordering = ('-sent',)

  def __str__(self):
    return self.to

  def Send(self):
    if self.sent:
      return ''

    return '<a href="./{}/send/" onclick="return confirm(\'Are you sure you want to send this invoice?\')">Send Invoice</a>'.format(
        self.id)

  Send.allow_tags = True

  def url(self):
    return reverse('conference-invoice', args=(self.key,))

  def Payment(self):
    if self.paid_on:
      return 'Paid: {}'.format(self.stripe_charge)

    return '<a href="{}" target="_blank">Payment Link</a>'.format(self.url())

  Payment.allow_tags = True

  def cents(self):
    return int(self.amount * 100)

  def send(self, request):
    url = 'http://'
    if request.is_secure():
      url = 'https://'

    url += request.get_host() + self.url()

    message = self.text
    message += '\n\n'
    message += url
    message += '\n\n'

    send_mail(self.subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              [self.to],
              fail_silently=False)
    self.sent = timezone.now()
    self.save()
