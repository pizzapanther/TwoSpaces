import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def startswith (value, snippet):
  return value.startswith(snippet)
  
@register.filter
def contains (value, snippet):
  return snippet in value
  
@register.filter
def add_class (widget, cls):
  widget = re.sub('^<(\S+)', '<\\1 class="%s"' % cls, str(widget))
  return mark_safe(widget)
  