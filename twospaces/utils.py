import csv
import codecs
import io
import types
import csv

from django import http
from django.utils import timezone


class CSVFileGenerator(object):
  mimeType = 'text/csv'
  queryset = None
  tags = []

  def __init__(self, queryset, tags, filename=None):
    self.queryset = queryset
    self.tags = tags
    if filename:
      self.filename = filename

    else:
      self.filename = self.queryset[0]._meta.object_name

  def generate(self):
    fh = io.StringIO()
    writer = csv.writer(fh)
    writer.writerow(self.tags)
    for item in self.queryset:
      current_row = []

      for tag in self.tags:
        value = getattr(item, tag)

        if callable(value):
          value = value()

        value = "{}".format(value)
        current_row.append(value)

      writer.writerow(current_row)

    return fh.getvalue()

  def getFileName(self):
    return self.filename + timezone.now().strftime("_%Y%m%d%H%M%S") + '.csv'

  def getIteratorResponse(self):
    response = http.HttpResponse(self.generate(), content_type=self.mimeType)
    response['Content-Disposition'
            ] = 'attachment; filename=' + self.getFileName()
    return response


class DynamicFieldsMixin(object):

  def __init__(self, *args, **kwargs):
    exclude = kwargs.pop('exclude', None)

    super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

    if exclude is not None:
      existing = set(self.fields.keys())
      for field_name in existing:
        if field_name in exclude:
          self.fields.pop(field_name)


PER_PAGE = 25


def paginate_queryset(request, queryset):
  page = request.GET.get('page', '1')
  try:
    page = int(page)

  except ValueError:
    raise http.Http404

  total = queryset.count()
  start = (page - 1) * PER_PAGE
  end = start + PER_PAGE

  next_page = None
  prev_page = None
  if page - 1 > 0:
    prev_page = page - 1

  if end < total:
    next_page = page + 1

  return queryset[start:end], page, next_page, prev_page
