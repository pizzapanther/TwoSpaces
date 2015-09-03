import traceback

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.template.response import TemplateResponse
from django.conf import settings
from django import http
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django import forms
from django.views.decorators.csrf import csrf_exempt

from twilio.rest import TwilioRestClient

from .models import User, SocialHandle, SMS


class SocialInline(admin.TabularInline):
  model = SocialHandle


class User2CreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ("username", "email", "verified_email")

  def clean_username(self):
    username = self.cleaned_data["username"]

    try:
      User._default_manager.get(username=username)

    except User.DoesNotExist:
      return username

    raise forms.ValidationError(self.error_messages['duplicate_username'],
                                code='duplicate_username')


class User2ChangeForm(UserChangeForm):

  class Meta:
    model = User
    fields = '__all__'


permission_required('profiles.change_user')


def send_sms_submit(request):
  phones = request.POST.getlist('phone')
  frm = request.POST.get('from')
  message = request.POST.get('message')

  client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,
                            settings.TWILIO_AUTH_TOKEN)

  for phone in phones:
    try:
      message = client.messages.create(to=phone, from_=frm, body=message)

    except:
      traceback.print_exc()
      messages.error(request, 'Error Sending {}'.format(phone))

  messages.success(request, 'SMS Sent!')
  return http.HttpResponseRedirect('/admin/profiles/user/')


def send_sms(modeladmin, request, queryset):
  context = {
      'queryset': queryset.exclude(phone__isnull=True),
      'title': 'Send SMS',
      'from': settings.TWILIO_NUMBERS
  }
  return TemplateResponse(request, 'admin/profiles/sms.html', context)


send_sms.short_description = "Send SMS"


class CurrentSpeakerFilter(admin.SimpleListFilter):
  title = 'Current Speaker'
  parameter_name = 'current'

  def lookups(self, request, model_admin):
    return (('1', 'Current Speakers'),)

  def queryset(self, request, queryset):
    if self.value() == '1':
      return queryset.filter(
          session__status='accepted',
          session__conference__slug=settings.DEFAULT_CONF).exclude(
              session__stype='lightning')


class User2Admin(UserAdmin):
  list_display = ('username', 'email', 'first_name', 'last_name', 'phone',
                  'current_speaker', 'is_staff', 'is_superuser')
  list_filter = (CurrentSpeakerFilter,)
  inlines = (SocialInline,)
  actions = (send_sms,)

  form = User2ChangeForm
  add_form = User2CreationForm

  fieldsets = (
      (None, {'fields': ('username', 'password')}), ('Personal info', {
          'fields': ('first_name', 'last_name', 'email', 'verified_email',
                     'phone', 'website', 'avatar', 'biography')
      }), ('Permissions',
           {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
      ('Important dates', {'fields': ('last_login', 'date_joined')}),)

  readonly_fields = ('last_login', 'date_joined')

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields':
          ('username', 'email', 'verified_email', 'password1', 'password2')
      }),)

  def current_speaker(self, obj):
    if obj.session_set.filter(status='accepted',
                              conference__slug=settings.DEFAULT_CONF).exclude(
                                  stype='lightning').count() > 0:
      return '<strong style="color: green;">&#10003;</strong>'

    return '<strong style="color: red;">&times;</strong>'

  current_speaker.allow_tags = True


class SMSForm(forms.ModelForm):
  frm = forms.CharField(label='From',
                        max_length=50,
                        initial=settings.TWILIO_NUMBERS[0])
  message = forms.CharField(
      max_length=140,
      widget=forms.TextInput(attrs={'style': 'width: 300px;'}))
  read = forms.BooleanField(required=False, initial=True)

  class Meta:
    model = SMS
    fields = ('to', 'frm', 'message', 'read', 'reply_to')


class SMSAdmin(admin.ModelAdmin):
  list_display = ('To', 'Frm', 'message', 'Type', 'read', 'created', 'reply')
  search_fields = ('to', 'frm', 'message')
  list_editable = ('read',)
  list_filter = ('read',)
  raw_id_fields = ('reply_to',)
  date_hierarchy = 'created'
  form = SMSForm

  def To(self, obj):
    if obj.to in settings.TWILIO_NUMBERS:
      return 'Conference'

    return obj.to

  def Frm(self, obj):
    if obj.frm in settings.TWILIO_NUMBERS:
      return 'Conference'

    return obj.frm

  def Type(self, obj):
    if obj.reply_to:
      return 'reply'

    elif obj.sms_set.all().count() > 0:
      return 'answered'

    return ''

  def reply(self, obj):
    if obj.frm not in settings.TWILIO_NUMBERS:
      return '<a href="/admin/profiles/sms/add/?reply_to={}&to={}">Reply &raquo;</a>'.format(
          obj.id, obj.frm)

    return ''

  reply.allow_tags = True

  def save_model(self, request, obj, form, change):
    if change:
      if 'read' in form.changed_data and len(form.changed_data) == 1:
        return super(SMSAdmin, self).save_model(request, obj, form, change)

      raise Exception("Changing Not Allowed")

    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,
                              settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=obj.to, from_=obj.frm, body=obj.message)
    if obj.reply_to:
      obj.reply_to.read = True
      obj.reply_to.save()

    return super(SMSAdmin, self).save_model(request, obj, form, change)


admin.site.register(User, User2Admin)
admin.site.register(SMS, SMSAdmin)


@csrf_exempt
def sms_sink(request):
  sid = request.POST.get('AccountSid')
  if sid == settings.TWILIO_ACCOUNT_SID:
    sms = SMS(
        to=request.POST.get('To').replace('+1', ''),
        frm=request.POST.get('From').replace('+1', ''),
        message=request.POST.get('Body'))
    sms.save()

  return http.HttpResponse('', content_type="text/plain")
