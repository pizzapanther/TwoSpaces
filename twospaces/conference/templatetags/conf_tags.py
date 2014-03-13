from django import template

register = template.Library()

@register.filter
def startswith (value, snippet):
  return value.startswith(snippet)
  
@register.filter
def contains (value, snippet):
  return snippet in value
  