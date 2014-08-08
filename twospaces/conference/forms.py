from django import forms

from .models import Sponsor, SponsorshipLevel, Session
from ..forms import BootstrapFormMixin

SESSION_TYPES = (
  ('talk-short', 'Short Talk (25 Minutes)'),
  ('talk-long', 'Talk (50 Minutes)'),
  ('tutorial', 'Tutorial (3 Hours)'),
)

class SponsorForm (forms.ModelForm):
  def __init__ (self, conf_id, *args, **kwargs):
    super(SponsorForm, self).__init__(*args, **kwargs)
    self.fields["level"].queryset = SponsorshipLevel.objects.filter(conference__id=conf_id)
    self.fields["name"].label = 'Company Name'
    self.fields["url"].label = 'URL (link people will be directed to)'
    self.fields["contact_name"].required = True
    self.fields["contact_phone"].required = True
    self.fields["contact_email"].required = True
    
  class Meta:
    model = Sponsor
    fields = ('name', 'url', 'contact_name', 'contact_phone', 'contact_email', 'level', 'logo')
    
class SessionForm (BootstrapFormMixin, forms.ModelForm):
  stype = forms.ChoiceField(choices=SESSION_TYPES, label="Session Type")
  
  class Meta:
    model = Session
    fields = ('name', 'stype', 'level', 'description', 'special_requirements')
    
class LightningSessionForm (BootstrapFormMixin, forms.ModelForm):
  class Meta:
    model = Session
    fields = ('name', 'description')
    