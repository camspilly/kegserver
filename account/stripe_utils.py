import stripe
from account.models import KegUser


def create_customer(card_token):
  stripe.api_key = "sk_test_ptBAeXjS5bQetoVHXbb3gpK6"
  customer = stripe.Customer.create(
    card=card_token # obtained with Stripe.js
  )
  return customer.id

def charge_customer(customer_id, amount):
  stripe.api_key = "sk_test_ptBAeXjS5bQetoVHXbb3gpK6"
  try:
    charge = stripe.Charge.create(
      amount= amount, # amount in cents, again
      currency="usd",
      customer=customer_id)
  except stripe.CardError, e:
    pass