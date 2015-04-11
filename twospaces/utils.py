import csv
import codecs
import io
import types

from django import http
from django.utils import timezone

class UnicodeWriter (object):
  """
  A CSV writer which will write rows to CSV file "f",
  which is encoded in the given encoding.
  """

  def __init__(self, dialect=csv.excel, encoding="utf-8", **kwds):
    # Redirect output to a queue
    self.queue = io.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.encoder = codecs.getincrementalencoder(encoding)()
    
  def encodeRow(self, row):
    self.writer.writerow([s.encode("utf-8") for s in row])
    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode("utf-8")
    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)
    # empty queue
    self.queue.truncate(0)
    
    return data
    
class CSVFileGenerator (object):
  mimeType = 'text/csv'
  encoder = UnicodeWriter(delimiter=',')
  queryset = None
  tags = []

  def __init__(self, queryset, tags, filename=None):
    self.queryset = queryset
    self.tags = tags
    if filename:
      self.filename = filename
      
    else:
      self.filename = self.queryset[0]._meta.object_name
      
  def _responseIterator(self):
    rows = []
    firstRow = self.tags
    rows.append(self.encoder.encodeRow(firstRow))
    for row in self.queryset:
      currentRow = []
      for tag in self.tags:
        value = getattr(row, tag)
        if callable(value):
          value = value()
          
        try:
          value = str(value)
          value = unicode(value.decode('utf-8'))
          
        except UnicodeEncodeError:
          value = unicode(value)
          
        currentRow.append(value)
        
      rows.append(self.encoder.encodeRow(currentRow))
      if len(rows) >= 100:
        yield ''.join(rows)
        rows = []
        
    if rows:
      yield ''.join(rows)
      
  def getFileName(self):
    return self.filename + timezone.now().strftime("_%Y%m%d%H%M%S") + '.csv'
    
  def getIteratorResponse(self):
    response = http.HttpResponse(self._responseIterator(), mimetype=self.mimeType)
    response['Content-Disposition'] = 'attachment; filename=' + self.getFileName()
    return response
    