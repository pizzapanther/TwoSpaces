
class BootstrapFormMixin (object):
  def __init__ (self, *args, **kwargs):
    super(BootstrapFormMixin, self).__init__(*args, **kwargs)
    for myField in self.fields:
      self.fields[myField].widget.attrs['class'] = 'form-control'
      