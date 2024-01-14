import os

import stripe

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Buyer
from carts.models import Cart, CartItem
from payments.models import Payment, PaymentItem


stripe.api_key = os.environ.get('STRIPE_API_KEY')
endpoint_secret = os.environ.get('ENDPOINT_SECRET')

def create_checkout_session(request):
  
  buyer = Buyer.objects.get(user=request.user)
  
  if buyer.payment_id == None:
    customer = stripe.Customer.create(
      address={
        'country': 'JP',
        'postal_code': '000-0000',
        'state': f'{buyer.address}_state',
        'city': f'{buyer.address}_city',
        'line1': f'{buyer.address}_line1',
        'line2': f'{buyer.address}_line2',
      },
      email=buyer.user.email,
      name=f'{buyer.last_name} {buyer.first_name}',
      phone=buyer.phone,
      shipping={
        'address': {
          'country': 'JP',
          'postal_code': '000-0000',
          'state': f'{buyer.address}_state_shipping',
          'city': f'{buyer.address}_city_shipping',
          'line1': f'{buyer.address}_line1_shipping',
          'line2': f'{buyer.address}_line2_shipping',
        },
        'name': f'{buyer.last_name} {buyer.first_name}',
      }
    )

    buyer.payment_id = customer.id
    buyer.save()
  
  payment_id = buyer.payment_id
  items = CartItem.objects.filter(cart=Cart.objects.get(buyer=buyer))
  
  li = []
  
  for item in items:
    i = {
      'price_data': {
        'currency': 'jpy',
        'product_data': {
          'name': item.product.name,
        },
        'unit_amount': item.product.price_with_tax,
        },
      'quantity': item.amount ,
      'adjustable_quantity': {
        'enabled': True,
      },
    }

    li.append(i)

  try:
    checkout_session = stripe.checkout.Session.create(
      line_items=li,
      mode='payment',
      success_url='http://127.0.0.1:8000/payments/checkout_success',
      cancel_url='http://127.0.0.1:8000/payments/checkout_cancel',
      shipping_address_collection={
              'allowed_countries': ['JP'],
            },
      payment_intent_data={"setup_future_usage": "on_session"},
      customer=payment_id,
    )
  except Exception as e:
    print('error')
    return e
  
  return redirect(checkout_session.url, code=303)


class PaymentSuccessView(TemplateView):
  template_name = 'payments/checkout_success.html'

class PaymentCancelView(TemplateView):
  template_name = 'payments/checkout_cancel.html'


@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.headers['STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    print('Invalid payload')
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e: # type: ignore
    print('Invalid signature')
    return HttpResponse(status=400)

  if event['type'] == 'checkout.session.completed':
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )

    fulfill_order(session)

  return HttpResponse(status=200)

def fulfill_order(session):
  buyer = Buyer.objects.get(payment_id=session.customer)
  address = session.shipping_details.address
  payment = Payment.objects.create(
    buyer=buyer,
    price=session.amount_total,
    shipping_name=f'{buyer.last_name} {buyer.first_name}',
    shipping_postal_code=address.postal_code,
    shipping_state=address.state,
    shipping_city=address.city,
    shipping_line1=address.line1,
    shipping_line2=address.line2,
  )
  payment.save()
  Cart.objects.get(buyer=buyer).delete()
  
  products = session.line_items.data
  
  for product in products:
    PaymentItem.objects.create(
    payment=payment,
    product=product.description,
    unit_price=product.price.unit_amount,
    amount=product.quantity,
    total_price=product.amount_total,
  ).save()
  
class PaymentListView(ListView):
  def get_queryset(self):
    buyer = Buyer.objects.get(user=self.request.user)
    payments = Payment.objects.filter(buyer=buyer)
    
    payment_list = []
    for payment in payments:
      payment_list.append(
        PaymentItem.objects.filter(payment=payment))
    return payment_list
  
  context_object_name = 'payments'
  template_name = 'payments/payment_list.html'