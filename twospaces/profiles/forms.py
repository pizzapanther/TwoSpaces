from django import forms
from django.core.urlresolvers import reverse_lazy
from django.forms.models import inlineformset_factory

from localflavor.us.forms import USPhoneNumberField
from django_markdown.widgets import MarkdownWidget

from .models import User, SocialHandle
from ..forms import BootstrapFormMixin

profile_url = reverse_lazy('profiles:profile')

class ResetForm (BootstrapFormMixin, forms.Form):
  password = forms.CharField(widget=forms.PasswordInput)
  password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
  
  def clean (self):
    cleaned_data = super(ResetForm, self).clean()
    
    if cleaned_data['password'] != cleaned_data['password2']:
      self._errors["password"] = self.error_class(['Passwords do not match.'])
      
    return cleaned_data
    
class ForgotForm (BootstrapFormMixin, forms.Form):
  username = forms.CharField(required=False)
  email = forms.EmailField(label='E-Mail', required=False)
  
  def clean (self):
    cleaned_data = super(ForgotForm, self).clean()
    username = cleaned_data.get('username', None)
    email = cleaned_data.get('email', None)
    
    if not username and not email:
      self._errors["email"] = self._errors["username"] = self.error_class(['Enter a username or e-mail'])
      
    if username:
      if User.objects.filter(username=username).count() == 0:
        self._errors["username"] = self.error_class(['Unknown username'])
        
    elif email:
      if User.objects.filter(email=email).count() == 0:
        self._errors["email"] = self.error_class(['Unknown e-mail'])
        
    return cleaned_data
    
class LoginForm (BootstrapFormMixin, forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  redirect = forms.CharField(initial="/", widget=forms.HiddenInput)
  
class SignupForm (BootstrapFormMixin, forms.ModelForm):
  phone = USPhoneNumberField(max_length=25, required=False, help_text="Optional: Used for conference SMS notifications.")
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
  phone = USPhoneNumberField(max_length=25, required=False, help_text="Optional: Used for conference SMS notifications.")
  
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'biography', 'website', 'avatar')
    widgets = {
      'biography': MarkdownWidget
    }
    
class SpeakerForm (BootstrapFormMixin, forms.ModelForm):
  phone = USPhoneNumberField(max_length=25, required=False, help_text="Used in case we need to contact you.")
  redirect = forms.CharField(initial=profile_url, widget=forms.HiddenInput)
  
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone', 'biography')
    widgets = {
      'biography': MarkdownWidget
    }
    
for f in ('first_name', 'last_name', 'phone', 'biography'):
  SpeakerForm.base_fields[f].required = True
  
class SocialHandleForm (BootstrapFormMixin, forms.ModelForm):
  class Meta:
    model = SocialHandle
    fields = ('site', 'username')
    
SocialHandleFormSet = inlineformset_factory(User, SocialHandle, form=SocialHandleForm, can_delete=True)
