from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, SocialHandle

class SocialInline (admin.TabularInline):
  model = SocialHandle
  
class User2CreationForm (UserCreationForm):
  class Meta:
    model = User
    fields = ("username", "email", "verified_email")
    
  def clean_username(self):
    username = self.cleaned_data["username"]
    
    try:
      User._default_manager.get(username=username)
      
    except User.DoesNotExist:
      return username
      
    raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')
    
class User2ChangeForm (UserChangeForm):
  class Meta:
    model = User
    fields = '__all__'
    
class User2Admin (UserAdmin):
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
  inlines = (SocialInline,)
  
  form = User2ChangeForm
  add_form = User2CreationForm
  
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'verified_email', 'website',
      ('photo', 'avatar'), 'biography')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )
  
  readonly_fields = ('last_login', 'date_joined')
  
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username', 'email', 'verified_email', 'password1', 'password2')}
    ),
  )
  
admin.site.register(User, User2Admin)
