import stripe
from account.models import KegUser

stripe.api_key = "sk_test_ptBAeXjS5bQetoVHXbb3gpK6"

def create_customer(card_token):
  customer = stripe.Customer.create(
    card="card_token" # obtained with Stripe.js
  )
  user = KegUser.objects.get(user = request.user)
  user.stripe_id = customer.id
  user.save()

def charge_customer(customer_id, amount):
  try:
    charge = stripe.Charge.create(
      amount= amount, # amount in cents, again
      currency="usd",
      customer=customer_id)
  except stripe.CardError, e:
    pass