from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone

import stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

from twospaces.conference.models import Invoice


@ensure_csrf_cookie
def invoice(request, key):
  invoice = get_object_or_404(Invoice, key=key, paid_on__isnull=True)

  if request.POST:
    invoice.paid_on = timezone.now()
    invoice.stripe_token = request.POST.get('stripeToken')
    charge = stripe.Charge.create(
        amount=invoice.cents(),
        currency="usd",
        card=invoice.stripe_token,
        description=invoice.name,
        receipt_email=invoice.to,)
    invoice.stripe_charge = charge['id']
    invoice.save()

    templates = ('conference/invoice-success.html')

  else:
    templates = ('conference/invoice.html')

  c = {
      'title': invoice.name,
      'invoice': invoice,
      'STRIPE_PUB_KEY': settings.STRIPE_PUB_KEY
  }
  return TemplateResponse(request, templates, context=c)
