from django import forms
from django.core.urlresolvers import reverse_lazy
from django.forms.models import inlineformset_factory

from localflavor.us.forms import USPhoneNumberField
from django_markdown.widgets import MarkdownWidget

from .models import User, SocialHandle
from ..forms import BootstrapFormMixin

profile_url = reverse_lazy('profiles:profile')

class LoginForm (BootstrapFormMixin, forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  redirect = forms.CharField(initial="/", widget=forms.HiddenInput)
  
class SignupForm (BootstrapFormMixin, forms.ModelForm):
  phone = USPhoneNumberField(max_length=25, required=False, help_text="Optional: Used for conference notifications.")
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)
  redirect = forms.CharField(initial=profile_url, widget=forms.HiddenInput)
  
  class Meta:
    model = User
    fields = ('username', 'email', 'phone', 'password')
    
  def clean_confirm_password (self):
    data = self.cleaned_data['confirm_password']
    if 'password' in self.cleaned_data:
      if data != self.cleaned_data['password']:
        raise forms.ValidationError("Password confirmation does not match!")
        
    return data
    
class ProfileForm (BootstrapFormMixin, forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'phone', 'biography', 'website', 'avatar')
    widgets = {
      'biography': MarkdownWidget
    }
    
class SocialHandleForm (BootstrapFormMixin, forms.ModelForm):
  class Meta:
    model = SocialHandle
    fields = ('site', 'username')
    
SocialHandleFormSet = inlineformset_factory(User, SocialHandle, form=SocialHandleForm, can_delete=True)
